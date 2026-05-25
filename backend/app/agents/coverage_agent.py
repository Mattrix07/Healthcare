"""Coverage Assessment Agent — HTTP dispatch or local demo output."""

from app.config import settings
from app.services.hosted_agents import invoke_hosted_agent
from app.agents.demo_outputs import build_demo_coverage_result


async def run_coverage_review(request_data: dict, clinical_findings: dict) -> dict:
    """Dispatch to the Coverage Assessment hosted agent or demo stub."""
    if settings.DEMO_MODE:
        return build_demo_coverage_result(request_data, clinical_findings)

    return await invoke_hosted_agent(
        "coverage-assessment-agent",
        settings.HOSTED_AGENT_COVERAGE_URL,
        {
            "request": request_data,
            "clinical_findings": clinical_findings,
        },
        foundry_agent_name=settings.HOSTED_AGENT_COVERAGE_NAME,
    )
