"""Clinical Reviewer Agent — local LLM, demo, or hosted dispatch."""

import logging

from app.config import settings
from app.services.hosted_agents import invoke_hosted_agent
from app.services.llm_client import generate_agent_json
from app.agents.demo_outputs import build_demo_clinical_result

logger = logging.getLogger(__name__)


async def run_clinical_review(request_data: dict) -> dict:
    """Run Clinical Reviewer Agent using local LLM, demo stub, or hosted agent."""
    template = build_demo_clinical_result(request_data)

    if settings.LOCAL_LLM_MODE:
        try:
            return await generate_agent_json(
                agent_name="Clinical Reviewer Agent",
                system_prompt=(
                    "You are a healthcare prior authorization clinical reviewer agent. "
                    "Extract clinical facts from the submitted notes, validate code format at a high level, "
                    "identify clinical rationale, prior treatments, severity, diagnostics, and gaps. "
                    "Do not invent external records or claim live database access. Do not make a final payer decision."
                ),
                payload=request_data,
                template=template,
            )
        except Exception as exc:
            logger.warning("Local LLM clinical agent failed; using demo output: %s", exc)
            return template

    if settings.DEMO_MODE:
        return template

    return await invoke_hosted_agent(
        "clinical-reviewer-agent",
        settings.HOSTED_AGENT_CLINICAL_URL,
        request_data,
        foundry_agent_name=settings.HOSTED_AGENT_CLINICAL_NAME,
    )
