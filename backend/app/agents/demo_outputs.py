"""Deterministic local demo outputs for the prior authorization workflow.

These helpers let the research prototype run visibly without Azure Foundry,
model deployments, MCP servers, or external credentials. They intentionally
return realistic, schema-shaped data so the existing frontend can show the
multi-agent workflow, agent details, decision rationale, and audit trail.
"""

from __future__ import annotations


def _codes(request_data: dict, key: str) -> list[str]:
    return [str(c).strip().upper() for c in request_data.get(key, []) if str(c).strip()]


def _procedure_summary(request_data: dict) -> str:
    procedures = _codes(request_data, "procedure_codes")
    if not procedures:
        return "requested procedure"
    return ", ".join(procedures)


def build_demo_compliance_result(request_data: dict) -> dict:
    """Return a realistic compliance checklist for local demonstrations."""
    missing_items: list[str] = []
    additional_info_requests: list[str] = []

    if not request_data.get("insurance_id"):
        missing_items.append("Insurance/member ID")
        additional_info_requests.append("Confirm active member eligibility and insurance/member ID.")

    notes = str(request_data.get("clinical_notes", "")).strip()
    if len(notes) < 80:
        missing_items.append("Detailed clinical notes")
        additional_info_requests.append("Submit fuller clinical notes supporting medical necessity.")

    overall_status = "complete" if not missing_items else "incomplete"

    checklist = [
        {
            "item": "Patient demographics present",
            "status": "complete",
            "detail": f"Patient and DOB captured for {request_data.get('patient_name', 'the member')}.",
        },
        {
            "item": "Provider NPI present",
            "status": "complete" if request_data.get("provider_npi") else "missing",
            "detail": f"Provider NPI: {request_data.get('provider_npi') or 'not supplied'}.",
        },
        {
            "item": "Diagnosis codes supplied",
            "status": "complete" if _codes(request_data, "diagnosis_codes") else "missing",
            "detail": f"Diagnosis codes: {', '.join(_codes(request_data, 'diagnosis_codes')) or 'none'}.",
        },
        {
            "item": "Procedure codes supplied",
            "status": "complete" if _codes(request_data, "procedure_codes") else "missing",
            "detail": f"Procedure codes: {_procedure_summary(request_data)}.",
        },
        {
            "item": "Clinical rationale documented",
            "status": "complete" if len(notes) >= 80 else "incomplete",
            "detail": "Clinical notes provide a reviewable rationale." if len(notes) >= 80 else "Clinical notes are brief and should be expanded.",
        },
        {
            "item": "Prior treatment history documented",
            "status": "complete" if any(term in notes.lower() for term in ["physio", "therapy", "medication", "conservative", "trial", "failed"]) else "incomplete",
            "detail": "Prior conservative treatment is referenced." if any(term in notes.lower() for term in ["physio", "therapy", "medication", "conservative", "trial", "failed"]) else "Prior treatment history is not clearly documented.",
        },
        {
            "item": "Supporting diagnostics referenced",
            "status": "complete" if any(term in notes.lower() for term in ["mri", "ct", "x-ray", "scan", "imaging", "lab"]) else "incomplete",
            "detail": "Supporting diagnostic evidence is referenced." if any(term in notes.lower() for term in ["mri", "ct", "x-ray", "scan", "imaging", "lab"]) else "No explicit diagnostic result is referenced.",
        },
        {
            "item": "Plan type identified",
            "status": "incomplete",
            "detail": "Demo mode assumes payer-specific policy must be confirmed by a human reviewer.",
        },
        {
            "item": "NCCI bundling risk considered",
            "status": "complete",
            "detail": "No obvious bundling issue detected in this demo review.",
        },
        {
            "item": "Service type classified",
            "status": "complete",
            "detail": "Request classified as prior authorization for a procedure/service.",
        },
    ]

    return {
        "agent_name": "Compliance Agent",
        "checklist": checklist,
        "overall_status": overall_status,
        "missing_items": missing_items,
        "additional_info_requests": additional_info_requests,
        "checks_performed": [
            {
                "rule": item["item"],
                "result": "pass" if item["status"] == "complete" else "warning",
                "detail": item["detail"],
            }
            for item in checklist
        ],
    }


def build_demo_clinical_result(request_data: dict) -> dict:
    """Return a realistic clinical review output for local demonstrations."""
    diagnosis_codes = _codes(request_data, "diagnosis_codes")
    procedure_codes = _codes(request_data, "procedure_codes")
    notes = str(request_data.get("clinical_notes", "")).strip()

    diagnosis_validation = [
        {
            "code": code,
            "valid": True,
            "description": "ICD-10 format accepted for demo review",
            "billable": "." in code or len(code) >= 3,
            "hierarchy_note": "Demo validation only; confirm official ICD-10 descriptor in production.",
        }
        for code in diagnosis_codes
    ]

    procedure_validation = [
        {
            "code": code,
            "valid": True,
            "description": "CPT/HCPCS format accepted by local preflight validation",
            "source": "orchestrator_preflight",
        }
        for code in procedure_codes
    ]

    return {
        "agent_name": "Clinical Reviewer Agent",
        "diagnosis_validation": diagnosis_validation,
        "procedure_validation": procedure_validation,
        "clinical_extraction": {
            "chief_complaint": "Prior authorization request requiring medical necessity review",
            "history_of_present_illness": notes[:500] or "Clinical notes were not provided in the demo request.",
            "prior_treatments": [
                "Conservative treatment history to be verified",
                "Medication/therapy response to be confirmed from submitted records",
            ],
            "severity_indicators": [
                "Symptoms or functional impact documented in clinical notes",
                "Procedure requested due to unresolved clinical need",
            ],
            "functional_limitations": [
                "Functional limitation requires reviewer confirmation from source documentation"
            ],
            "diagnostic_findings": [
                "Diagnostic evidence referenced or required for payer criteria assessment"
            ],
            "duration_and_progression": "Duration/progression should be confirmed from provider records.",
            "medical_history_and_comorbidities": "Demo mode does not access external EHR history.",
            "extraction_confidence": 78,
        },
        "literature_support": [
            {
                "title": "Evidence review placeholder for requested service",
                "pmid": "DEMO-PMID",
                "relevance": "Represents where PubMed evidence would be surfaced in a production workflow.",
            }
        ],
        "clinical_trials": [],
        "clinical_summary": (
            "Demo clinical review completed. The submitted request contains reviewable clinical information, "
            "but a human reviewer should confirm payer-specific medical necessity evidence before final determination."
        ),
        "tool_results": [
            {
                "tool_name": "icd10_validation_demo",
                "status": "pass",
                "detail": f"{len(diagnosis_codes)}/{len(diagnosis_codes)} diagnosis codes accepted in demo validation.",
            },
            {
                "tool_name": "clinical_extraction_demo",
                "status": "pass",
                "detail": "Clinical facts extracted from submitted notes without external EHR access.",
            },
        ],
        "checks_performed": [
            {
                "rule": "Diagnosis-code validation",
                "result": "pass",
                "detail": "Diagnosis codes were structurally valid for demo purposes.",
            },
            {
                "rule": "Clinical-evidence extraction",
                "result": "pass",
                "detail": "Key review facts were extracted from the submitted notes.",
            },
        ],
    }


def build_demo_coverage_result(request_data: dict, clinical_findings: dict) -> dict:
    """Return a realistic coverage review output for local demonstrations."""
    procedure_codes = _codes(request_data, "procedure_codes")
    diagnosis_codes = _codes(request_data, "diagnosis_codes")

    criteria_assessment = [
        {
            "criterion": "Member eligibility and provider participation",
            "status": "MET" if request_data.get("insurance_id") else "INSUFFICIENT",
            "confidence": 72 if request_data.get("insurance_id") else 45,
            "evidence": [
                "Insurance/member ID supplied" if request_data.get("insurance_id") else "Insurance/member ID missing"
            ],
            "notes": "Production workflow would verify eligibility against payer systems.",
            "source": "demo_policy_check",
            "met": bool(request_data.get("insurance_id")),
        },
        {
            "criterion": "Procedure is potentially coverable under medical-necessity policy",
            "status": "MET",
            "confidence": 76,
            "evidence": [f"Requested procedure code(s): {', '.join(procedure_codes) or 'not supplied'}"],
            "notes": "Demo assumes the requested service can be reviewed under a payer medical policy.",
            "source": "demo_policy_check",
            "met": True,
        },
        {
            "criterion": "Clinical documentation supports requested service",
            "status": "INSUFFICIENT",
            "confidence": 58,
            "evidence": [
                clinical_findings.get("clinical_summary", "Clinical summary unavailable")
                if isinstance(clinical_findings, dict) else "Clinical findings unavailable"
            ],
            "notes": "Reviewer should confirm prior treatments, diagnostic findings, and severity criteria.",
            "source": "demo_policy_check",
            "met": False,
        },
    ]

    documentation_gaps = [
        {
            "what": "Payer-specific medical necessity documentation",
            "critical": True,
            "request": "Confirm failed conservative therapy, diagnostic evidence, duration, and severity criteria from source records.",
        }
    ]
    if not request_data.get("insurance_id"):
        documentation_gaps.append({
            "what": "Active member eligibility",
            "critical": True,
            "request": "Provide insurance/member ID or eligibility confirmation.",
        })

    return {
        "agent_name": "Coverage Agent",
        "provider_verification": {
            "npi": str(request_data.get("provider_npi", "")),
            "name": "Demo Provider / Facility",
            "specialty": "Specialty pending NPI registry verification",
            "status": "VERIFIED" if request_data.get("provider_npi") else "not_found",
            "detail": "Demo mode does not call the live NPI registry.",
        },
        "coverage_policies": [
            {
                "policy_id": "DEMO-LCD-001",
                "title": "Representative medical necessity policy for requested service",
                "type": "LCD/NCD placeholder",
                "relevant": True,
            }
        ],
        "criteria_assessment": criteria_assessment,
        "coverage_criteria_met": [
            item["criterion"] for item in criteria_assessment if item["status"] == "MET"
        ],
        "coverage_criteria_not_met": [
            item["criterion"] for item in criteria_assessment if item["status"] != "MET"
        ],
        "policy_references": ["DEMO-LCD-001: Representative payer medical necessity criteria"],
        "coverage_limitations": [
            "Demo mode uses representative criteria only; production requires payer-specific policy lookup."
        ],
        "documentation_gaps": documentation_gaps,
        "tool_results": [
            {
                "tool_name": "npi_verification_demo",
                "status": "pass" if request_data.get("provider_npi") else "warning",
                "detail": "Provider NPI captured; live NPI verification skipped in demo mode.",
            },
            {
                "tool_name": "coverage_policy_demo",
                "status": "warning",
                "detail": "Representative coverage criteria applied; payer-specific policy not queried.",
            },
        ],
        "checks_performed": [
            {
                "rule": item["criterion"],
                "result": "pass" if item["status"] == "MET" else "warning",
                "detail": item["notes"],
            }
            for item in criteria_assessment
        ],
    }


def build_demo_synthesis_result(
    request_data: dict,
    compliance_result: dict,
    clinical_result: dict,
    coverage_result: dict,
    cpt_validation: dict | None = None,
) -> dict:
    """Return a final decision synthesis for local demonstrations."""
    cpt_ok = bool((cpt_validation or {}).get("valid", True))
    provider_ok = bool(coverage_result.get("provider_verification", {}).get("npi"))
    criteria = coverage_result.get("criteria_assessment", [])
    unmet = [c.get("criterion", "Unnamed criterion") for c in criteria if c.get("status") != "MET"]
    gaps = coverage_result.get("documentation_gaps", [])

    approve = cpt_ok and provider_ok and not unmet and not gaps
    recommendation = "approve" if approve else "pend_for_review"
    confidence = 0.86 if approve else 0.68
    confidence_level = "HIGH" if approve else "MEDIUM"

    missing_documentation = [
        gap.get("what", "Additional documentation") for gap in gaps if isinstance(gap, dict)
    ]

    return {
        "recommendation": recommendation,
        "confidence": confidence,
        "confidence_level": confidence_level,
        "summary": (
            "Demo synthesis recommends approval based on the visible criteria."
            if approve else
            "Demo synthesis recommends pending the request for human review because one or more coverage or documentation criteria require confirmation."
        ),
        "clinical_rationale": clinical_result.get(
            "clinical_summary",
            "Clinical rationale generated from submitted notes in demo mode.",
        ),
        "decision_gate": (
            "GATE 1 (Provider): PASS | GATE 2 (Codes): PASS | GATE 3 (Medical necessity): PASS"
            if approve else
            "GATE 1 (Provider): PASS | GATE 2 (Codes): PASS | GATE 3 (Medical necessity): PEND"
        ),
        "coverage_criteria_met": coverage_result.get("coverage_criteria_met", []),
        "coverage_criteria_not_met": coverage_result.get("coverage_criteria_not_met", unmet),
        "missing_documentation": missing_documentation,
        "documentation_gaps": gaps,
        "policy_references": coverage_result.get("policy_references", []),
        "criteria_summary": f"{len(coverage_result.get('coverage_criteria_met', []))} of {len(criteria)} criteria met; remaining items require reviewer confirmation.",
        "synthesis_audit_trail": {
            "mode": "local_demo",
            "cpt_preflight_valid": cpt_ok,
            "provider_present": provider_ok,
            "unmet_or_insufficient_criteria": unmet,
            "documentation_gaps": missing_documentation,
        },
        "disclaimer": (
            "Local demo output only. This is not a clinical, legal, or payer determination. "
            "A human reviewer must validate source documentation and payer-specific policy before any decision."
        ),
    }
