from github import Github
import httpx
import os

g = Github(os.getenv("GITHUB_TOKEN"))

async def fetch_pr_data(pr_url: str) -> dict:
    # parse URL
    parts = pr_url.replace("https://github.com/", "").split("/")
    owner, repo_name, _, pr_number = parts[0], parts[1], parts[2], int(parts[3])

    repo = g.get_repo(f"{owner}/{repo_name}")
    pr = repo.get_pull(pr_number)

    async with httpx.AsyncClient() as client:
        diff_response = await client.get(
            pr.url,
            headers={
                "Authorization": f"token {os.getenv('GITHUB_TOKEN')}",
                "Accept": "application/vnd.github.v3.diff"
            }
        )
        diff_response.raise_for_status()

    return {
        "title": pr.title,
        "description": pr.body or "",
        "author": pr.user.login,
        "files_changed": [f.filename for f in pr.get_files()],
        "diff": diff_response.text,
        "repo_url": f"https://github.com/{owner}/{repo_name}"
    }