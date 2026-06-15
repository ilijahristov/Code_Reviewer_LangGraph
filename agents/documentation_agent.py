from state import AgentState
from config import model
from models import DocumentationReview
from langchain_core.messages import HumanMessage

async def documentation_agent(state: AgentState) -> dict:
    """
    Evaluates the documentation quality of the changes in the pull request.
    Checks for missing docstrings, README updates, and docs that are out of sync.
    """

    prompt = f"""You are a documentation review agent.
    Analyze this pull request and evaluate the quality of its documentation.

    Focus on:
    - New or changed functions/classes that are missing docstrings
    - Whether the README needs updating to reflect these changes
    - Existing documentation (docstrings, comments, README sections) that is now
      out of sync with the new code behavior
    - Overall clarity and completeness of any documentation that was added

    Pull request information:
    - PR Title: {state['title']}
    - PR Description: {state['description']}
    - Files Changed: {state['files_changed']}
    - Diff: {state['diff']}
    """

    structured_model = model.with_structured_output(DocumentationReview)
    response = await structured_model.ainvoke([HumanMessage(content=prompt)])

    return {"documentation_agent_summary": response}