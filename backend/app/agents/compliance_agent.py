"""Compliance Validation Agent — local LLM, demo, or hosted dispatch."""

import logging

from app.config import settings
from app.services.hosted_agents import invoke_hosted_agent
from app.services.llm_client import generate_agent_json
from app.agents.demo_outputs import build_demo_compliance_result

logger = logging.getLogger(__name__)


async def run_compliance_review(request_data: dict) -> dict:
    """Run Compliance Agent using local LLM, demo stub, or hosted agent."""
    template = build_demo_compliance_result(request_data)

    if settings.LOCAL_LLM_MODE:
        try:
            return await generate_agent_json(
                agent_name="Compliance Agent",
                system_prompt=(
                    "You are a healthcare prior authorization compliance agent. "
                    "Review whether the request has enough administrative and documentation detail for payer review. "
                    "Focus on completeness, missing items, and next information requests. "
                    "Do not make a final clinical or payment decision."
                ),
                payload=request_data,
                template=template,
            )
        except Exception as exc:
            logger.warning("Local LLM compliance agent failed; using demo output: %s", exc)
            return template

    if settings.DEMO_MODE:
        return template

    return await invoke_hosted_agent(
        "compliance-agent",
        settings.HOSTED_AGENT_COMPLIANCE_URL,
        request_data,
        foundry_agent_name=settings.HOSTED_AGENT_COMPLIANCE_NAME,
    )
