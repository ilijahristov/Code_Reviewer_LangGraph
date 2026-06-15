# Pull Request Code Reviewer LangGraph

This is a simple app built on LangGraph that takes in a url of a PR request and returns the overview for that request.

## Structure

```
         FastAPI
            ↓
        fetch_node
      ↙     ↓     ↘
changes   docs  test_coverage
      ↘     ↓     ↙
      summary_agent
            ↓
        db_save_node
            ↓
           END
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
    author: str
    repo_url: str

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

#### Test Coverage Agent

Evaluates whether the changes in the pull request have sufficient test coverage, and if the tests are well-designed and comprehensive.

### db_save_node.py

After the summary agent completes, the graph routes to `db_save_node` before ending. This node persists the full review to PostgreSQL — it checks whether the repository already exists in the `repositories` table and creates it if not, then inserts the review into `pr_reviews`.

```
         FastAPI
            ↓
        fetch_node
      ↙     ↓     ↘
changes   docs  test_coverage
      ↘     ↓     ↙
      summary_agent
            ↓
        db_save_node
            ↓
           END
```

### Checkpointing

The graph uses LangGraph's PostgreSQL checkpointer. After every node execution the full state is snapshotted to the database. The checkpoint tables are created automatically on server startup by LangGraph checkpoint library.

Each request generates a unique `thread_id` which is returned in the API response alongside the review. This ID can be used with `inspect_state.py` to replay the full execution history.

### Database Schema

You need to create the following two tables in your PostgreSQL database before running the server. The checkpoint tables are handled automatically.

```sql
CREATE TABLE repositories (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(90) UNIQUE NOT NULL,
    url VARCHAR(150) UNIQUE NOT NULL
);

CREATE TABLE pr_reviews (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    repository_id INTEGER NOT NULL REFERENCES repositories(id),
    pr_url VARCHAR(150) UNIQUE NOT NULL,
    pr_number INTEGER NOT NULL,
    author VARCHAR(90),
    title VARCHAR(255),
    changes_summary TEXT,
    documentation_summary TEXT,
    test_coverage_summary TEXT,
    final_summary TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Inspecting Graph State

`inspect_state.py` is a standalone script for inspecting checkpoint history stored in the database.

```bash
# lists all threads, then prompts you to pick one
python inspect_state.py

# jump straight to a specific thread
python inspect_state.py <thread_id>
```

It prints a step-by-step breakdown of the graph execution — which node ran at each step and what the state looked like — followed by the final state and what node would run next. Useful for debugging failed or incomplete runs.


## Installation & Setup LangGraph Agent
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
DATABASE_URL=your_postgresql_connection_string_here
```
### 5. Run the server
```bash
uvicorn main:app --reload
```
The API will be available at http://127.0.0.1:8000.

### Usage
Send a POST request to the /review endpoint with a GitHub PR URL:

```bash
curl -X POST "http://127.0.0.1:8000/review?pr_url=https://github.com/owner/repo/pull/123"
```
Or open the interactive docs at http://127.0.0.1:8000/docs.


## Installation & Setup Frontend

### 1. Clone the repository if you havent from the langgraph installation
```bash
git clone https://github.com/your-username/Code_Reviewer_LangGraph.git
cd Code_Reviewer_LangGraph
```

### 2. Install modules
```bash
cd frontend
npm install
```

### 3. Run frontend server
```bash
npm run dev
```