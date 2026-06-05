from fastapi import FastAPI
from graph import app



"""This is the main entry point for the application.
It sets up the FastAPI server
and defines the endpoint for reviewing pull requests.
FastAPI post call -> /review -> app.run() -> graph execution -> returns review summary
"""

api = FastAPI()

@api.post("/review")
async def review_pr(pr_url: str):
    """
    Endpoint to review a pull request.
    """
    result = await app.ainvoke({"pr_url": pr_url})
    return {"review_summary": result}