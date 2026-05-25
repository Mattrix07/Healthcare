"""Synthesis Decision Agent — HTTP dispatch or local demo output."""

from app.config import settings
from app.services.hosted_agents import invoke_hosted_agent
from app.agents.demo_outputs import build_demo_synthesis_result


async def run_synthesis_review(
    request_data: dict,
    compliance_result: dict,
    clinical_result: dict,
    coverage_result: dict,
    cpt_validation: dict | None = None,
) -> dict:
    """Dispatch to the Synthesis Decision hosted agent or demo stub."""
    if settings.DEMO_MODE:
        return build_demo_synthesis_result(
            request_data=request_data,
            compliance_result=compliance_result,
            clinical_result=clinical_result,
            coverage_result=coverage_result,
            cpt_validation=cpt_validation,
        )

    return await invoke_hosted_agent(
        "synthesis-decision-agent",
        settings.HOSTED_AGENT_SYNTHESIS_URL,
        {
            "request": request_data,
            "compliance_result": compliance_result,
            "clinical_result": clinical_result,
            "coverage_result": coverage_result,
            "cpt_validation": cpt_validation,
        },
        foundry_agent_name=settings.HOSTED_AGENT_SYNTHESIS_NAME,
    )
