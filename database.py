import asyncpg
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

pool = None

async def init_pool():
    global pool
    if pool is None:
        pool = await asyncpg.create_pool(
            os.getenv("DATABASE_URL"),
            min_size=2,
            max_size=10
        )

async def create_repository(conn, name: str, url: str) -> int:
    await conn.execute(
        """
        INSERT INTO repositories (name, url)
        VALUES ($1, $2)
        ON CONFLICT (url) DO NOTHING
        """,
        name, url
    )
    row = await conn.fetchrow("SELECT id FROM repositories WHERE url = $1", url)
    return row["id"]

async def save_review(state: dict):
    await init_pool()
    async with pool.acquire() as conn:
        repo_url = state["repo_url"]
        repo_name = repo_url.rstrip("/").split("/")[-1]

        repository_id = await create_repository(conn, repo_name, repo_url)

        pr_url = state["pr_url"]
        pr_number = int(pr_url.rstrip("/").split("/")[-1])

        await conn.execute(
            """
            INSERT INTO pr_reviews (
                repository_id, pr_url, pr_number, author, title,
                changes_summary, documentation_summary,
                test_coverage_summary, final_summary
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            ON CONFLICT (pr_url) DO NOTHING
            """,
            repository_id,
            pr_url,
            pr_number,
            state.get("author"),
            state.get("title"),
            state.get("changes_agent_summary"),
            state.get("documentation_agent_summary"),
            state.get("test_coverage_agent_summary"),
            state.get("summary_agent_review"),
        )
