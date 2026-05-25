import os
from dotenv import load_dotenv

load_dotenv()


def _env_bool(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def _env_float(name: str, default: str) -> float:
    try:
        return float(os.getenv(name, default))
    except ValueError:
        return float(default)


class Settings:
    FRONTEND_ORIGIN: str = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

    # Local research/demo mode: deterministic schema-shaped demo outputs.
    DEMO_MODE: bool = _env_bool("DEMO_MODE", "false")

    # Local LLM mode: calls an OpenAI-compatible Chat Completions endpoint.
    LOCAL_LLM_MODE: bool = _env_bool("LOCAL_LLM_MODE", "false")
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "")
    LLM_TEMPERATURE: float = _env_float("LLM_TEMPERATURE", "0.2")

    HOSTED_AGENT_CLINICAL_URL: str = os.getenv("HOSTED_AGENT_CLINICAL_URL", "")
    HOSTED_AGENT_COMPLIANCE_URL: str = os.getenv("HOSTED_AGENT_COMPLIANCE_URL", "")
    HOSTED_AGENT_COVERAGE_URL: str = os.getenv("HOSTED_AGENT_COVERAGE_URL", "")
    HOSTED_AGENT_SYNTHESIS_URL: str = os.getenv("HOSTED_AGENT_SYNTHESIS_URL", "")

    AZURE_AI_PROJECT_ENDPOINT: str = os.getenv("AZURE_AI_PROJECT_ENDPOINT", "")
    HOSTED_AGENT_CLINICAL_NAME: str = os.getenv(
        "HOSTED_AGENT_CLINICAL_NAME", "clinical-reviewer-agent"
    )
    HOSTED_AGENT_COMPLIANCE_NAME: str = os.getenv(
        "HOSTED_AGENT_COMPLIANCE_NAME", "compliance-agent"
    )
    HOSTED_AGENT_COVERAGE_NAME: str = os.getenv(
        "HOSTED_AGENT_COVERAGE_NAME", "coverage-assessment-agent"
    )
    HOSTED_AGENT_SYNTHESIS_NAME: str = os.getenv(
        "HOSTED_AGENT_SYNTHESIS_NAME", "synthesis-agent"
    )

    HOSTED_AGENT_TIMEOUT_SECONDS: float = float(
        os.getenv("HOSTED_AGENT_TIMEOUT_SECONDS", "180")
    )

    HOSTED_AGENT_AUTH_HEADER: str = os.getenv("HOSTED_AGENT_AUTH_HEADER", "Authorization")
    HOSTED_AGENT_AUTH_SCHEME: str = os.getenv("HOSTED_AGENT_AUTH_SCHEME", "Bearer")
    HOSTED_AGENT_AUTH_TOKEN: str = os.getenv("HOSTED_AGENT_AUTH_TOKEN", "")

    APPLICATION_INSIGHTS_CONNECTION_STRING: str = os.getenv(
        "APPLICATION_INSIGHTS_CONNECTION_STRING", ""
    )


settings = Settings()
