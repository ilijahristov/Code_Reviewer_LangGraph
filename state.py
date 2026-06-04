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
    performance_review: str
    style_review: str
    summary: str
    final_report: str