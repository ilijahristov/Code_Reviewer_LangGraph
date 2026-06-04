from state import AgentState
from config import model
from langchain_core.messages import HumanMessage

def test_coverage_agent(state: AgentState) -> str:
    """
    Evaluates wether the changes in the pull request have sufficient test coverage, 
    and if the tests are well-designed and comprehensive.
    """
    
    prompt = f"""You are a test coverage review agent.
    Your task is to analyze the changes in a pull request
    and evaluate the test coverage related to those changes.
    Wether the changes are sufficiently covered by tests,
    and if the tests are well-designed and comprehensive.
    
    Here is the information about the pull request:
    - PR Title: {state['title']}
    - PR Description: {state['description']}
    - Diff: {state['diff']}
    - Files Changed: {state['files_changed']}
    """
    
    response = model([HumanMessage(content=prompt)])
    
    return {"test_coverage_agent_summary": response.content}