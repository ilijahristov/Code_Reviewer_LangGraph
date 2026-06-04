from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    
    messages: Annotated[Sequence[BaseMessage], add_messages]
    pr_url: str          
    title: str           
    description: str       
    diff: str            
    files_changed: list  
    changes_agent_summary: str
    documentation_agent_summary: str
    test_coverage_agent_summary: str
    summary_agent_summary: str