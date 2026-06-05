from tools.github_fetch import fetch_pr_data

def fetch_node(state: dict) -> dict:
    """
    Fetches the pull request data and populates the state.
    """
    pr_url = state.get("pr_url")
    if not pr_url:
        raise ValueError("PR URL is missing in the state.")
    
    return fetch_pr_data(pr_url)