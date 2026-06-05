from state import AgentState
from config import model
from langchain_core.messages import HumanMessage

def summary_agent(state: AgentState) -> str:
    
    """
    End point summary agent that reviews the summaries from the other agents 
    and synthesizes them into an overall review of the pull request.
    """
    
    prompt = f"""You are a summary review agent. 
    Your task is to review the summaries from the other agents,
    look for any contradictions or discrepancies between them,
    and synthesize the information into a coherent overall summary of the pull request review.
    
    Here are the summaries from the other agents:
    - Changes Agent Summary: {state['changes_agent_summary']}
    - Documentation Agent Summary: {state['documentation_agent_summary']}
    - Test Coverage Agent Summary: {state['test_coverage_agent_summary']}
    
    Please provide an overall summary of the pull request review, highlighting any key issues, strengths, or areas for improvement.
    """
    
    response = model([HumanMessage(content=prompt)])
    
    return {"summary_agent_review": response.content}