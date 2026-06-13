from pydantic import BaseModel, Field
from typing import Literal


class ChangesReview(BaseModel):
    severity: Literal["low", "medium", "high", "critical"] = Field(
        description="Overall severity of the breaking or risky changes detected"
    )
    api_changes: list[str] = Field(
        description="Public API modifications (function signatures, return types, endpoints)"
    )
    schema_changes: list[str] = Field(
        description="Database schema changes (new columns, dropped tables, index modifications)"
    )
    removed_symbols: list[str] = Field(
        description="Functions, classes, or exports that were removed or renamed"
    )
    config_changes: list[str] = Field(
        description="Configuration format or key changes that could break deployments"
    )
    findings: list[str] = Field(
        description="Other concerns that could break dependent systems"
    )
    blocking: bool = Field(
        description="True if any finding is severe enough to block merging"
    )
    summary: str = Field(
        description="One or two sentence prose summary of the overall risk"
    )


class DocumentationReview(BaseModel):
    severity: Literal["low", "medium", "high"] = Field(
        description="How serious the documentation gaps are"
    )
    missing_docstrings: list[str] = Field(
        description="New or changed functions/classes that lack docstrings"
    )
    readme_update_needed: bool = Field(
        description="True if the README should be updated to reflect these changes"
    )
    outdated_docs: list[str] = Field(
        description="Existing documentation that is now out of sync with the code"
    )
    findings: list[str] = Field(
        description="Other documentation quality issues (clarity, completeness, accuracy)"
    )
    blocking: bool = Field(
        description="True if documentation gaps are severe enough to block merging"
    )
    summary: str = Field(
        description="One or two sentence prose summary of the documentation quality"
    )


class TestCoverageReview(BaseModel):
    severity: Literal["low", "medium", "high"] = Field(
        description="How serious the test coverage gaps are"
    )
    coverage_verdict: Literal["sufficient", "partial", "insufficient"] = Field(
        description="Overall verdict on whether the changes are adequately tested"
    )
    untested_changes: list[str] = Field(
        description="Changed code paths or functions that have no corresponding tests"
    )
    test_quality_issues: list[str] = Field(
        description="Existing or new tests that are poorly designed, fragile, or incomplete"
    )
    findings: list[str] = Field(
        description="Other test-related concerns (missing edge cases, missing integration tests)"
    )
    blocking: bool = Field(
        description="True if coverage gaps are severe enough to block merging"
    )
    summary: str = Field(
        description="One or two sentence prose summary of the test coverage state"
    )


class OverallReview(BaseModel):
    overall_severity: Literal["low", "medium", "high", "critical"] = Field(
        description="Highest severity across all specialist reviews"
    )
    verdict: Literal["approve", "request_changes", "needs_discussion"] = Field(
        description="Final merge recommendation"
    )
    blocking: bool = Field(
        description="True if any specialist review flagged a blocker"
    )
    key_issues: list[str] = Field(
        description="The most important problems that must be addressed"
    )
    strengths: list[str] = Field(
        description="Things the PR does well"
    )
    recommendations: list[str] = Field(
        description="Concrete, actionable improvements the author should make"
    )
    summary: str = Field(
        description="Two to three sentence overall assessment of the pull request"
    )
