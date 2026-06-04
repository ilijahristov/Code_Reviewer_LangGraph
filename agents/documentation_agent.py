from state import AgentState
from config import model
from langchain_core.messages import HumanMessage

def documentation_agent(state: AgentState) -> str:
    """
    Evaluates the documentation quality of the changes in the pull request.
    Wether a README or docstring is needed, and if the existing documentation files are clear and sufficient.
    """
    prompt = f"""You are a documentation review agent. 
    Your task is to analyze the changes in a pull request
    and evaluate the quality of the documentation related to those changes.
    
    Here is the information about the pull request:
    - PR Title: {state['title']}
    - PR Description: {state['description']}
    - Diff: {state['diff']}
    - Files Changed: {state['files_changed']}
    
    Please provide feedback on whether the documentation is clear, sufficient, and if any improvements are needed.
    """
    
    response = model([HumanMessage(content=prompt)])
    
    return {"documentation_agent_summary": response.content}