# Pull Request Code Reviewer LangGraph

This is a simple app built on LangGraph that takes in a url of a PR request and returns the overview for that request.

## Structure

```
FastAPI → fetch_node ─┬→ changes_agent ───────┬→ summary_agent → END
                      ├→ documentation_agent ─┤
                      └→ test_coverage_agent ─┘

```

A Pull Request URL(ex. https://github.com/owner/repo/pull/pr_id_number) is inputted via FastAPI which gets stored in state, then fetch_node reads from state pr_url and uses the Github API to get the data about the pull request.

### fetch_node.py

This is the Start node of the graph here the job of this node is to get the information about the Pull Request via the Github API. it does so by calling the `fetch_pr_data(pr_url: str)` function inside github_fetch.py, the function returns the populated state:
```python
"title": pr.title,
        "description": pr.body or "",
        "author": pr.user.login,
        "files_changed": [f.filename for f in pr.get_files()],
        "diff": diff_response.text
```

### State

The state stores information about the sequence of messages for same session, data fields used by the agents, and the summary returns from the agents themselves

```python
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
    # data fields for the code review process
    pr_url: str          
    title: str           
    description: str       
    diff: str            
    files_changed: list  
    
    # summaries from agents
    changes_agent_summary: str
    documentation_agent_summary: str
    test_coverage_agent_summary: str
    summary_agent_review: str
```


### Agents

After we've populated the state and the fetch_node gets the return from `fetch_pr_data(pr_url)` the graph execution continues to the agents, all agents return their summaries which are stored in the state.

#### Changes Agent

Detects if the PR changes public APIs, modifies database schemas,
removes functions other code might depend on,
or changes configuration formats. Flags anything that could break other systems.

#### Documentation Agent

Evaluates the documentation quality of the changes in the pull request.

####

Evaluates wether the changes in the pull request have sufficient test coverage, and if the tests are well-designed and comprehensive.


## Installation & Setup
### Prerequisites
- Python 3.10+
- A GitHub account with a personal access token
- An Anthropic API key

### 1. Clone the repository
```bash
git clone https://github.com/your-username/Code_Reviewer_LangGraph.git
cd Code_Reviewer_LangGraph
```
### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a .env file in the project root:
```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
GITHUB_TOKEN=your_github_token_here
```
### 5. Run the server
```bash
uvicorn main:api --reload
```
The API will be available at http://127.0.0.1:8000.

### Usage
Send a POST request to the /review endpoint with a GitHub PR URL:

```bash
curl -X POST "http://127.0.0.1:8000/review?pr_url=https://github.com/owner/repo/pull/123"
```
Or open the interactive docs at http://127.0.0.1:8000/docs.
