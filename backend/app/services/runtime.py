"""Runtime-mode helpers for demo, local LLM, and hosted-agent operation."""

from app.config import settings

_ALLOWED_MODES = {"demo", "llm", "hosted", "auto"}


def get_runtime_mode() -> str:
    """Return the effective runtime mode.

    RUNTIME_MODE is the preferred switch. RUNTIME_MODE=auto keeps the original
    DEMO_MODE / LOCAL_LLM_MODE behaviour for older local setups.
    """
    configured = (settings.RUNTIME_MODE or "demo").strip().lower()
    if configured not in _ALLOWED_MODES:
        configured = "demo"

    if configured != "auto":
        return configured

    if settings.LOCAL_LLM_MODE:
        return "llm"
    if settings.DEMO_MODE:
        return "demo"
    return "hosted"


def use_demo_mode() -> bool:
    return get_runtime_mode() == "demo"


def use_llm_mode() -> bool:
    return get_runtime_mode() == "llm"


def use_hosted_mode() -> bool:
    return get_runtime_mode() == "hosted"
