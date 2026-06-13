from github import Github, GithubException
import httpx
import os
from fastapi import HTTPException

g = Github(os.getenv("GITHUB_TOKEN"))

async def fetch_pr_data(pr_url: str) -> dict:
    try:
        parts = pr_url.replace("https://github.com/", "").split("/")
        owner, repo_name, _, pr_number = parts[0], parts[1], parts[2], int(parts[3])
    except (IndexError, ValueError):
        raise HTTPException(status_code=400, detail=f"Malformed PR URL: {pr_url!r}")

    try:
        repo = g.get_repo(f"{owner}/{repo_name}")
        pr = repo.get_pull(pr_number)
        files_changed = [f.filename for f in pr.get_files()]
    except GithubException as exc:
        if exc.status == 404:
            raise HTTPException(status_code=404, detail="Repository or PR not found")
        raise HTTPException(status_code=exc.status, detail=exc.data.get("message", str(exc)))

    try:
        async with httpx.AsyncClient() as client:
            diff_response = await client.get(
                pr.url,
                headers={
                    "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
                    "Accept": "application/vnd.github.v3.diff"
                }
            )
            diff_response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise HTTPException(
            status_code=exc.response.status_code,
            detail=f"GitHub diff fetch failed: {exc.response.text}"
        )

    return {
        "title": pr.title,
        "description": pr.body or "",
        "author": pr.user.login,
        "files_changed": files_changed,
        "diff": diff_response.text,
        "repo_url": f"https://github.com/{owner}/{repo_name}"
    }