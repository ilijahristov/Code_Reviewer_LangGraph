import psycopg
import psycopg_pool
import os
import json

from dotenv import load_dotenv, find_dotenv
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

load_dotenv(find_dotenv())

pool = None

async def init_pool():
    global pool
    if pool is None:
        pool = psycopg_pool.AsyncConnectionPool(
            os.getenv("DATABASE_URL"),
            min_size=2,
            max_size=10,
            open=False
        )
        await pool.open()

async def get_checkpointer():
    await init_pool()
    async with await psycopg.AsyncConnection.connect(
        os.getenv("DATABASE_URL"), autocommit=True
    ) as setup_conn:
        await AsyncPostgresSaver(setup_conn).setup()
    return AsyncPostgresSaver(pool)

async def create_repository(conn, name: str, url: str) -> int:
    await conn.execute(
        """
        INSERT INTO repositories (name, url)
        VALUES (%s, %s)
        ON CONFLICT (url) DO NOTHING
        """,
        (name, url)
    )
    cur = await conn.execute("SELECT id FROM repositories WHERE url = %s", (url,))
    row = await cur.fetchone()
    return row[0]

def _parse_json(val):
    """Summary columns are stored as JSON strings; decode them for the API."""
    if val is None:
        return None
    try:
        return json.loads(val)
    except (TypeError, json.JSONDecodeError):
        return val


async def list_repositories() -> list[dict]:
    """All repositories, used to populate the sidebar chat list."""
    await init_pool()
    async with pool.connection() as conn:
        cur = await conn.execute(
            "SELECT id, name, url FROM repositories ORDER BY name"
        )
        rows = await cur.fetchall()
        return [{"id": r[0], "name": r[1], "url": r[2]} for r in rows]


async def get_reviews_by_repo_name(name: str) -> list[dict]:
    """Every review for one repository, oldest first (one chat thread)."""
    await init_pool()
    async with pool.connection() as conn:
        cur = await conn.execute(
            """
            SELECT pr.pr_url, pr.pr_number, pr.title, pr.author, pr.created_at,
                   pr.final_summary, pr.changes_summary,
                   pr.documentation_summary, pr.test_coverage_summary
            FROM pr_reviews pr
            JOIN repositories repo ON repo.id = pr.repository_id
            WHERE repo.name = %s
            ORDER BY pr.created_at ASC
            """,
            (name,)
        )
        rows = await cur.fetchall()
        return [
            {
                "pr_url": r[0],
                "pr_number": r[1],
                "title": r[2],
                "author": r[3],
                "created_at": r[4].isoformat() if r[4] else None,
                "final_summary": _parse_json(r[5]),
                "changes_summary": _parse_json(r[6]),
                "documentation_summary": _parse_json(r[7]),
                "test_coverage_summary": _parse_json(r[8]),
            }
            for r in rows
        ]


async def save_review(state: dict):
    await init_pool()
    async with pool.connection() as conn:
        repo_url = state["repo_url"]
        repo_name = repo_url.rstrip("/").split("/")[-1]

        repository_id = await create_repository(conn, repo_name, repo_url)

        pr_url = state["pr_url"]
        pr_number = int(pr_url.rstrip("/").split("/")[-1])

        def _serialize(obj) -> str | None:
            return obj.model_dump_json() if obj is not None else None

        await conn.execute(
            """
            INSERT INTO pr_reviews (
                repository_id, pr_url, pr_number, author, title,
                changes_summary, documentation_summary,
                test_coverage_summary, final_summary
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (pr_url) DO NOTHING
            """,
            (
                repository_id,
                pr_url,
                pr_number,
                state.get("author"),
                state.get("title"),
                _serialize(state.get("changes_agent_summary")),
                _serialize(state.get("documentation_agent_summary")),
                _serialize(state.get("test_coverage_agent_summary")),
                _serialize(state.get("summary_agent_review")),
            )
        )
