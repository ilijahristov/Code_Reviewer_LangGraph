from typing import TypedDict, Annotated, Sequence, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from models import ChangesReview, DocumentationReview, TestCoverageReview, OverallReview

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

    # structured outputs from agents
    changes_agent_summary: Optional[ChangesReview]
    documentation_agent_summary: Optional[DocumentationReview]
    test_coverage_agent_summary: Optional[TestCoverageReview]
    summary_agent_review: Optional[OverallReview]