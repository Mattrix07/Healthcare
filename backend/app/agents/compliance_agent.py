"""Compliance Validation Agent — HTTP dispatch or local demo output."""

from app.config import settings
from app.services.hosted_agents import invoke_hosted_agent
from app.agents.demo_outputs import build_demo_compliance_result


async def run_compliance_review(request_data: dict) -> dict:
    """Dispatch to the Compliance Validation hosted agent or demo stub."""
    if settings.DEMO_MODE:
        return build_demo_compliance_result(request_data)

    return await invoke_hosted_agent(
        "compliance-agent",
        settings.HOSTED_AGENT_COMPLIANCE_URL,
        request_data,
        foundry_agent_name=settings.HOSTED_AGENT_COMPLIANCE_NAME,
    )
