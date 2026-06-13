from state import AgentState
from config import model
from models import ChangesReview
from langchain_core.messages import HumanMessage

async def changes_agent(state: AgentState) -> dict:
    """
    Detects if the PR changes public APIs, modifies database schemas,
    removes functions other code might depend on,
    or changes configuration formats. Flags anything that could break other systems.
    """

    prompt = f"""You are a code changes review agent.
    Analyze this pull request and identify anything that could break dependent systems.

    Focus on:
    - Public API changes (function signatures, endpoints, return types)
    - Database schema changes (new/dropped columns, tables, indexes)
    - Removed or renamed symbols (functions, classes, exports) that callers may depend on
    - Configuration format changes that could break deployments

    Pull request information:
    - PR Title: {state['title']}
    - PR Description: {state['description']}
    - Files Changed: {state['files_changed']}
    - Diff:
    {state['diff']}
    """

    structured_model = model.with_structured_output(ChangesReview)
    response = await structured_model.ainvoke([HumanMessage(content=prompt)])

    return {"changes_agent_summary": response}