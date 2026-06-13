from state import AgentState
from config import model
from models import TestCoverageReview
from langchain_core.messages import HumanMessage

async def test_coverage_agent(state: AgentState) -> dict:
    """
    Evaluates whether the changes in the pull request have sufficient test coverage,
    and whether the tests are well-designed and comprehensive.
    """

    prompt = f"""You are a test coverage review agent.
    Analyze this pull request and evaluate the quality and completeness of its tests.

    Focus on:
    - Changed or new code paths that have no corresponding tests
    - Tests that are poorly designed: brittle assertions, no edge cases,
      testing implementation details instead of behavior
    - Missing integration or end-to-end test coverage for significant changes
    - Whether the overall coverage verdict is sufficient, partial, or insufficient

    Pull request information:
    - PR Title: {state['title']}
    - PR Description: {state['description']}
    - Files Changed: {state['files_changed']}
    - Diff:
    {state['diff']}
    """

    structured_model = model.with_structured_output(TestCoverageReview)
    response = await structured_model.ainvoke([HumanMessage(content=prompt)])

    return {"test_coverage_agent_summary": response}