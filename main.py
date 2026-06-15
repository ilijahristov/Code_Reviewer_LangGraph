from fastapi import FastAPI
from contextlib import asynccontextmanager
import uuid
import graph
from database import init_pool



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
