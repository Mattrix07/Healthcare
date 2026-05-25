"""Clinical Reviewer Agent — HTTP dispatch or local demo output."""

from app.config import settings
from app.services.hosted_agents import invoke_hosted_agent
from app.agents.demo_outputs import build_demo_clinical_result


async def run_clinical_review(request_data: dict) -> dict:
    """Dispatch to the Clinical Reviewer hosted agent or demo stub."""
    if settings.DEMO_MODE:
        return build_demo_clinical_result(request_data)

    return await invoke_hosted_agent(
        "clinical-reviewer-agent",
        settings.HOSTED_AGENT_CLINICAL_URL,
        request_data,
        foundry_agent_name=settings.HOSTED_AGENT_CLINICAL_NAME,
    )
