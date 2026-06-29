"""Markdown report generation for GeoCase AI."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    from .risk_screening import PROJECT_ROOT, screen_site
except ImportError:
    from risk_screening import PROJECT_ROOT, screen_site


REPORTS_DIR = PROJECT_ROOT / "reports"


def generate_report(result: dict[str, Any]) -> str:
    """Generate a one-page markdown GIS risk screening report."""
    if result["status"] != "success":
        return f"# GeoCase AI Risk Screening Report\n\nError: {result['message']}\n"

    reasons_text = "\n".join(f"- {reason}" for reason in result["reasons"])

    return f"""# GeoCase AI Risk Screening Report

## Site Information

- Site name: {result["site_name"]}
- Address: {result["address"]}
- Project type: {result["project_type"]}
- Coordinates: {result["lat"]}, {result["lon"]}

## GIS Risk Summary

- Flood risk: {result["flood_risk"]}
- Extreme rainfall risk: {result["rainfall_risk"]}
- Noise risk: {result["noise_risk"]}
- Environmental justice flag: {result["ej_flag"]}
- Poverty rate: {result["poverty_rate"]:.0%}
- Minority population share: {result["minority_share"]:.0%}
- Distance to school: {result["near_school_m"]} meters
- Distance to major transit: {result["near_transit_m"]} meters
- Distance to river or waterway: {result["near_river_m"]} meters

## Overall Assessment

- Risk score: {result["risk_score"]}
- Overall risk level: {result["overall_risk"]}
- Reviewer queue: {result["reviewer_queue"]}

## Key Reasons

{reasons_text}

## Recommended Next Step

{result["next_step"]}

## AI Planning Explanation

{result["ai_explanation"]}

## Prototype Data Note

This prototype uses a sample geospatial risk dataset for demonstration. In production, the same workflow can connect to FEMA flood data, Census ACS demographics, NOAA rainfall data, USGS data, OpenStreetMap, and local municipal GIS portals.

## Responsible Use Note

This screening report is intended to support early-stage planning review. Final decisions should be made by qualified human reviewers.
"""


def generate_case_report(case: dict[str, Any]) -> str:
    """Generate a markdown report that includes case and human review details."""
    result = case["screening_result"]
    if result["status"] != "success":
        return f"""# GeoCase AI Risk Screening Report

## Case Information

- Case ID: {case["case_id"]}
- Case name: {case["case_name"]}
- Status: {case["status"]}
- Workflow path: {case["workflow_path"]}

## Screening Error

{result["message"]}

## Recommended Next Step

{case["case_decision"]}
"""

    base_report = generate_report(result)
    human_review = case.get("human_review")
    if human_review:
        review_text = f"""## Human Reviewer Decision

- Reviewer: {human_review["reviewer_name"]}
- Decision: {human_review["decision"]}
- Reviewed at: {human_review["reviewed_at"]}
- Notes: {human_review["notes"] or "No notes provided"}
"""
    else:
        review_text = f"""## Human Reviewer Decision

- Required: {"Yes" if case["human_review_required"] else "No"}
- Assigned queue: {case["human_review_task"] or "None"}
- Decision: {case["case_decision"]}
"""

    case_header = f"""# GeoCase AI Case Review Report

## Case Information

- Case ID: {case["case_id"]}
- Case name: {case["case_name"]}
- Project name: {case["project_name"]}
- Submitted address: {case["address"]}
- Project type: {case["project_type"]}
- Reviewer team: {case["reviewer"]}
- Status: {case["status"]}
- Workflow path: {case["workflow_path"]}
- Created at: {case["created_at"]}
- Updated at: {case["updated_at"]}

"""
    return case_header + base_report.replace("# GeoCase AI Risk Screening Report\n\n", "") + "\n" + review_text


def write_report(query: str, output_path: str | Path | None = None) -> Path:
    """Screen a site and write its markdown report."""
    result = screen_site(query)
    report = generate_report(result)
    REPORTS_DIR.mkdir(exist_ok=True)
    if output_path is None:
        filename = f"{query.strip().replace(' ', '_')}_report.md"
        output_path = REPORTS_DIR / filename
    output = Path(output_path)
    output.write_text(report, encoding="utf-8")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a GeoCase AI report.")
    parser.add_argument("query", nargs="?", help="Planning site name or address")
    parser.add_argument("--output", help="Output markdown report path")
    args = parser.parse_args()

    query = args.query or input("Enter site name or address: ")
    output_path = write_report(query, args.output)
    print(f"Report generated: {output_path}")


if __name__ == "__main__":
    main()
