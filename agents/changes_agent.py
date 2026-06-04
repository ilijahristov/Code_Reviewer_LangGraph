from state import AgentState

def changes_agent(state: AgentState) -> str:
    """
    Change Agent
    Detects if the PR changes public APIs, modifies database schemas,
    removes functions other code might depend on,
    or changes configuration formats. Flags anything that could break other systems.
    """