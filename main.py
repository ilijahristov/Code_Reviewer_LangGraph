from fastapi import FastAPI
from contextlib import asynccontextmanager
from graph import app as graph
from database import init_pool



"""This is the main entry point for the application.
It sets up the FastAPI server
and defines the endpoint for reviewing pull requests.
FastAPI post call -> /review -> app.run() -> graph execution -> returns review summary
"""

@asynccontextmanager
async def lifespan(app):
    await init_pool()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/review")
async def review_pr(pr_url: str):
    """
    Endpoint to review a pull request.
    """
    result = await graph.ainvoke({"pr_url": pr_url})
    return {"review_summary": result}