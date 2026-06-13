from state import AgentState
from config import model
from langchain_core.messages import HumanMessage

async def changes_agent(state: AgentState) -> str:
    """
    Change Agent
    Detects if the PR changes public APIs, modifies database schemas,
    removes functions other code might depend on,
    or changes configuration formats. Flags anything that could break other systems.
    """
    
    prompt = f"""You are a code changes review agent. 
    Your task is to analyze the changes in a pull request
    and identify any potential issues or improvements
    related to the code changes.
    
    Here is the information about the pull request:
    - PR Title: {state['title']}
    - PR Description: {state['description']}
    - Diff: {state['diff']}
    - Files Changed: {state['files_changed']}
    """
    
    response = await model.ainvoke([HumanMessage(content=prompt)])

    return {"changes_agent_summary": response.content}