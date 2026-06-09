import asyncio
import sys
import os
import psycopg
import psycopg.rows
import psycopg_pool
from dotenv import load_dotenv, find_dotenv
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

load_dotenv(find_dotenv())

DATABASE_URL = os.getenv("DATABASE_URL")

TRUNCATE_AT = 200


def truncate(value: str) -> str:
    if len(value) > TRUNCATE_AT:
        return value[:TRUNCATE_AT] + f"... [{len(value) - TRUNCATE_AT} chars truncated]"
    return value


def print_state(state: dict):
    LONG_FIELDS = {"diff", "changes_agent_summary", "documentation_agent_summary",
                   "test_coverage_agent_summary", "summary_agent_review", "description"}
    for key, val in state.items():
        if key == "messages":
            print(f"  messages: [{len(val)} message(s)]")
        elif isinstance(val, str) and key in LONG_FIELDS:
            print(f"  {key}: {truncate(val)}")
        elif isinstance(val, list):
            print(f"  {key}: {val}")
        else:
            print(f"  {key}: {val}")


async def list_threads(conn):
    async with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
        await cur.execute(
            """
            SELECT thread_id, MAX(checkpoint_id) AS last_checkpoint
            FROM checkpoints
            GROUP BY thread_id
            ORDER BY last_checkpoint DESC
            """
        )
        rows = await cur.fetchall()
    if not rows:
        print("No threads found in checkpoints table.")
        return []
    print(f"\n{'#':<4} {'THREAD ID':<40} {'LAST CHECKPOINT'}")
    print("-" * 80)
    for i, row in enumerate(rows):
        print(f"{i+1:<4} {row['thread_id']:<40} {row['last_checkpoint']}")
    return [row["thread_id"] for row in rows]


def infer_node(metadata: dict, updated_channels: list) -> str:
    source = metadata.get("source", "")
    if source == "input":
        return "INPUT"

    updated = set(updated_channels)
    has_branch = any(ch.startswith("branch:to:") for ch in updated)

    if not has_branch:
        return "db_save_node"
    if "branch:to:fetch_node" in updated:
        return "START"
    if "diff" in updated and "branch:to:changes_agent" in updated:
        return "fetch_node"
    if "branch:to:summary_agent" in updated:
        return "changes_agent / documentation_agent / test_coverage_agent"
    if "branch:to:db_save_node" in updated:
        return "summary_agent"
    return "unknown"


def infer_next(history: list) -> list:
    final = history[0]
    updated = set(final.checkpoint.get("updated_channels", []))
    channel_values = final.checkpoint.get("channel_values", {})

    pending_branches = [
        ch.replace("branch:to:", "")
        for ch, val in channel_values.items()
        if ch.startswith("branch:to:") and val is not None
    ]
    if pending_branches:
        return pending_branches

    if "branch:to:db_save_node" in updated or "db_save_node" in infer_node(final.metadata, list(updated)):
        return ["END"]

    return ["END"]


async def inspect_thread(checkpointer: AsyncPostgresSaver, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}

    history = [s async for s in checkpointer.alist(config)]

    if not history:
        print(f"\nNo checkpoints found for thread: {thread_id}")
        return

    print(f"\n{'='*70}")
    print(f"THREAD: {thread_id}")
    print(f"Total checkpoints: {len(history)}")
    print(f"{'='*70}")

    for checkpoint_tuple in reversed(history):
        metadata = checkpoint_tuple.metadata or {}
        step = metadata.get("step", "?")
        updated = checkpoint_tuple.checkpoint.get("updated_channels", [])
        node = infer_node(metadata, updated)

        print(f"\n--- Step {step}: [{node}] ---")
        print_state(checkpoint_tuple.checkpoint.get("channel_values", {}))

    final = history[0]
    next_nodes = infer_next(history)
    print(f"\n{'='*70}")
    print(f"FINAL STATE (after last checkpoint)")
    print(f"{'='*70}")
    print_state(final.checkpoint.get("channel_values", {}))
    print(f"\nNext node(s): {next_nodes}")


async def main():
    pool = psycopg_pool.AsyncConnectionPool(
        DATABASE_URL, min_size=1, max_size=5, open=False
    )
    await pool.open()

    checkpointer = AsyncPostgresSaver(pool)

    async with await psycopg.AsyncConnection.connect(DATABASE_URL) as raw_conn:
        thread_ids = await list_threads(raw_conn)

    if not thread_ids:
        await pool.close()
        return

    if len(sys.argv) > 1:
        thread_id = sys.argv[1]
        print(f"\nUsing thread_id from argument: {thread_id}")
    else:
        print("\nEnter a thread_id from the list above (or paste any thread_id): ", end="")
        thread_id = input().strip()

    if not thread_id:
        print("No thread_id provided, exiting.")
        await pool.close()
        return

    await inspect_thread(checkpointer, thread_id)
    await pool.close()


if __name__ == "__main__":
    asyncio.run(main())
