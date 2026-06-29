"""Case workflow orchestration for the GeoCase AI demo."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .report_generator import generate_case_report
from .risk_screening import PROJECT_ROOT, screen_site


CASE_STORE_PATH = PROJECT_ROOT / "data" / "case_store.json"
CASE_REPORTS_DIR = PROJECT_ROOT / "reports" / "cases"

REVIEW_DECISIONS = {
    "Approve with mitigation",
    "Request additional environmental study",
    "Escalate to senior reviewer",
    "Reject recommendation",
}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _load_cases() -> list[dict[str, Any]]:
    if not CASE_STORE_PATH.exists():
        return []
    return json.loads(CASE_STORE_PATH.read_text(encoding="utf-8"))


def _save_cases(cases: list[dict[str, Any]]) -> None:
    CASE_STORE_PATH.parent.mkdir(exist_ok=True)
    CASE_STORE_PATH.write_text(json.dumps(cases, indent=2), encoding="utf-8")


def _next_case_id(cases: list[dict[str, Any]]) -> str:
    return f"GEO-{len(cases) + 1:04d}"


def _report_path(case_id: str) -> Path:
    return CASE_REPORTS_DIR / f"{case_id}_risk_screening_report.md"


def _route_for_risk(result: dict[str, Any]) -> dict[str, Any]:
    risk = result["overall_risk"]
    if risk == "Low":
        return {
            "workflow_path": "Low Risk Auto Recommendation",
            "status": "Closed - Auto Recommendation Generated",
            "human_review_required": False,
            "human_review_task": None,
            "case_decision": "Automatic low-risk recommendation",
        }
    if risk == "Medium":
        return {
            "workflow_path": "Planner Manual Review",
            "status": "Awaiting Planner Review",
            "human_review_required": True,
            "human_review_task": "Planner Review Task",
            "case_decision": "Pending human decision",
        }
    return {
        "workflow_path": "Environmental Justice Review",
        "status": "Awaiting Environmental Justice Review",
        "human_review_required": True,
        "human_review_task": "Environmental Justice Review Task",
        "case_decision": "Pending human decision",
    }


def create_case(
    project_name: str,
    address: str,
    project_type: str,
    reviewer: str,
) -> dict[str, Any]:
    """Create a planning case, run screening, route it, and generate a report."""
    cases = _load_cases()
    case_id = _next_case_id(cases)
    created_at = _now()
    result = screen_site(address)

    if result["status"] != "success":
        case = {
            "case_id": case_id,
            "case_name": project_name,
            "project_name": project_name,
            "address": address,
            "project_type": project_type,
            "reviewer": reviewer,
            "status": "Address Match Failed",
            "workflow_path": "Exception Handling",
            "created_at": created_at,
            "updated_at": created_at,
            "screening_result": result,
            "human_review_required": False,
            "human_review_task": None,
            "human_review": None,
            "case_decision": "Request corrected address or additional GIS data",
            "report_path": None,
        }
        cases.append(case)
        _save_cases(cases)
        return case

    route = _route_for_risk(result)
    case = {
        "case_id": case_id,
        "case_name": project_name,
        "project_name": project_name,
        "address": address,
        "project_type": project_type or result["project_type"],
        "reviewer": reviewer,
        "status": route["status"],
        "workflow_path": route["workflow_path"],
        "created_at": created_at,
        "updated_at": created_at,
        "screening_result": result,
        "human_review_required": route["human_review_required"],
        "human_review_task": route["human_review_task"],
        "human_review": None,
        "case_decision": route["case_decision"],
        "report_path": str(_report_path(case_id)),
    }
    write_case_report(case)
    cases.append(case)
    _save_cases(cases)
    return case


def list_cases() -> list[dict[str, Any]]:
    """Return all stored demo cases."""
    return _load_cases()


def get_case(case_id: str) -> dict[str, Any] | None:
    """Return a single stored demo case."""
    for case in _load_cases():
        if case["case_id"] == case_id:
            return case
    return None


def submit_human_review(
    case_id: str,
    decision: str,
    notes: str,
    reviewer_name: str,
) -> dict[str, Any] | None:
    """Record the reviewer decision and close the human review step."""
    if decision not in REVIEW_DECISIONS:
        raise ValueError(f"Unsupported review decision: {decision}")

    cases = _load_cases()
    for case in cases:
        if case["case_id"] != case_id:
            continue

        reviewed_at = _now()
        case["human_review"] = {
            "decision": decision,
            "notes": notes,
            "reviewer_name": reviewer_name,
            "reviewed_at": reviewed_at,
        }
        case["case_decision"] = decision
        case["status"] = "Human Review Completed"
        case["updated_at"] = reviewed_at
        write_case_report(case)
        _save_cases(cases)
        return case
    return None


def write_case_report(case: dict[str, Any]) -> Path:
    """Write the latest report for a case."""
    CASE_REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path = _report_path(case["case_id"])
    path.write_text(generate_case_report(case), encoding="utf-8")
    case["report_path"] = str(path)
    return path
