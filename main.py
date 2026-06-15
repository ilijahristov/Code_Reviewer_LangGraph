from fastapi import FastAPI
from contextlib import asynccontextmanager
import uuid
import graph
from database import init_pool, list_repositories, get_reviews_by_repo_name



"""This is the main entry point for the application.
It sets up the FastAPI server
and defines the endpoint for reviewing pull requests.
FastAPI post call -> /review -> app.run() -> graph execution -> returns review summary
"""

@asynccontextmanager
async def lifespan(app):
    await graph.build_graph()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/review")
async def review_pr(pr_url: str):
    thread_id = str(uuid.uuid4())
    result = await graph.app.ainvoke(
        {"pr_url": pr_url},
        config={"configurable": {"thread_id": thread_id}}
    )
    return {"review_summary": result, "thread_id": thread_id}

@app.post("/review/{thread_id}")
async def continue_review(thread_id: str, pr_url: str):
    result = await graph.app.ainvoke(
        {"pr_url": pr_url},
        config={"configurable": {"thread_id": thread_id}}
    )
    return {"review_summary": result, "thread_id": thread_id}


# --- Read endpoints used by the frontend ---

@app.get("/repositories")
async def get_repositories():
    """Sidebar chat list: all repositories that have been reviewed."""
    return await list_repositories()


@app.get("/repositories/{name}/reviews")
async def get_repository_reviews(name: str):
    """Chat history for one repository (its reviews, oldest first)."""
    return await get_reviews_by_repo_name(name)
