from langgraph.graph import StateGraph, START, END

from state import AgentState
from tools.fetch_node import fetch_node
from tools.db_save_node import save_node

from agents.changes_agent import changes_agent
from agents.documentation_agent import documentation_agent
from agents.test_coverage_agent import test_coverage_agent
from agents.summary_agent import summary_agent

"""
A graph that represents the state of a code review process.
each node in the graph represents a specific aspect of the code review, such as:
- Code changes
- Documentation
- Test coverage
- Overall summary

FastAPI → fetch_node ─┬→ changes_agent ────uv───┬→ summary_agent → END
                      ├→ documentation_agent ─┤
                      └→ test_coverage_agent ─┘

"""
    
# graph
graph = StateGraph(AgentState)

# nodes
graph.add_node("fetch_node", fetch_node)  # This node is responsible for fetching the pull request data and populating the state.
graph.add_node("changes_agent", changes_agent)
graph.add_node("documentation_agent", documentation_agent)
graph.add_node("test_coverage_agent", test_coverage_agent)
graph.add_node("summary_agent", summary_agent)
graph.add_node("db_save_node", save_node)

# edges
graph.add_edge(START, "fetch_node")
graph.add_edge("fetch_node", "changes_agent")
graph.add_edge("fetch_node", "documentation_agent")
graph.add_edge("fetch_node", "test_coverage_agent")

graph.add_edge("changes_agent", "summary_agent")
graph.add_edge("documentation_agent", "summary_agent")
graph.add_edge("test_coverage_agent", "summary_agent")

graph.add_edge("summary_agent", "db_save_node")
graph.add_edge("db_save_node", END)

app = graph.compile()