import json
from state import AgentState
from config import model
from models import OverallReview
from langchain_core.messages import HumanMessage

async def summary_agent(state: AgentState) -> dict:
    """
    Synthesizes the structured outputs from all specialist agents into a
    single overall review of the pull request.
    """

    def _render(obj) -> str:
        return json.dumps(obj.model_dump(), indent=2) if obj else "not available"

    prompt = f"""You are a summary review agent.
    Synthesize the structured reviews from three specialist agents into a single
    overall assessment. Look for patterns across the reviews — do multiple agents
    flag the same area? Are there contradictions? Is anything a hard blocker?

    Changes review:
    {_render(state.get('changes_agent_summary'))}

    Documentation review:
    {_render(state.get('documentation_agent_summary'))}

    Test coverage review:
    {_render(state.get('test_coverage_agent_summary'))}
    """

    structured_model = model.with_structured_output(OverallReview)
    response = await structured_model.ainvoke([HumanMessage(content=prompt)])

    return {"summary_agent_review": response}