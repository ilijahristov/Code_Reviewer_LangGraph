import psycopg
import psycopg_pool
import os

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
