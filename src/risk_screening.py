"""Core GIS risk screening logic for GeoCase AI."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CSV_PATH = PROJECT_ROOT / "data" / "sample_sites.csv"

RISK_SCORE = {
    "Low": 1,
    "Medium": 2,
    "High": 3,
}


def load_sites(csv_path: str | Path = DEFAULT_CSV_PATH) -> pd.DataFrame:
    """Load the prototype GIS screening dataset."""
    return pd.read_csv(csv_path)


def find_site(query: str, sites: pd.DataFrame) -> dict[str, Any] | None:
    """Find the first sample site whose name or address contains the query."""
    query_lower = query.strip().lower()
    if not query_lower:
        return None

    matches = sites[
        sites["address"].str.lower().str.contains(query_lower, na=False, regex=False)
        | sites["site_name"].str.lower().str.contains(query_lower, na=False, regex=False)
    ]
    if matches.empty:
        return None
    return matches.iloc[0].to_dict()


def calculate_risk(site: dict[str, Any]) -> dict[str, Any]:
    """Calculate the rule-based screening score and routing decision."""
    score = 0
    reasons: list[str] = []

    for field in ("flood_risk", "rainfall_risk", "noise_risk"):
        score += RISK_SCORE.get(str(site[field]), 0)

    if site["flood_risk"] == "High":
        reasons.append("High flood exposure")
    elif site["flood_risk"] == "Medium":
        reasons.append("Moderate flood exposure")

    if site["rainfall_risk"] == "High":
        reasons.append("High extreme rainfall exposure")
    elif site["rainfall_risk"] == "Medium":
        reasons.append("Moderate extreme rainfall exposure")

    if site["noise_risk"] == "High":
        reasons.append("High noise exposure")
    elif site["noise_risk"] == "Medium":
        reasons.append("Moderate noise exposure")

    if site["ej_flag"] == "Yes":
        score += 2
        reasons.append("Environmental justice flag is present")
    if site["poverty_rate"] > 0.25:
        score += 1
        reasons.append("Poverty rate is above the screening threshold")
    if site["minority_share"] > 0.60:
        score += 1
        reasons.append("Minority population share is above the screening threshold")
    if site["near_school_m"] < 500:
        score += 1
        reasons.append("Site is within 500 meters of a school")
    if site["near_transit_m"] < 200:
        score += 1
        reasons.append("Site is within 200 meters of major transit infrastructure")
    if site["near_river_m"] < 500:
        score += 1
        reasons.append("Site is within 500 meters of a river or waterway")

    if score >= 11:
        overall_risk = "High"
        next_step = "Route to environmental justice reviewer"
        reviewer_queue = "Environmental Justice Review"
    elif score >= 7:
        overall_risk = "Medium"
        next_step = "Route to planner for manual review"
        reviewer_queue = "Planner Review"
    else:
        overall_risk = "Low"
        next_step = "Generate automatic low-risk recommendation"
        reviewer_queue = "No manual review required"

    explanation = build_ai_explanation(site, overall_risk, reasons)

    return {
        "site_name": site["site_name"],
        "address": site["address"],
        "project_type": site["project_type"],
        "lat": site["lat"],
        "lon": site["lon"],
        "flood_risk": site["flood_risk"],
        "rainfall_risk": site["rainfall_risk"],
        "noise_risk": site["noise_risk"],
        "poverty_rate": site["poverty_rate"],
        "minority_share": site["minority_share"],
        "near_school_m": site["near_school_m"],
        "near_transit_m": site["near_transit_m"],
        "near_river_m": site["near_river_m"],
        "ej_flag": site["ej_flag"],
        "risk_score": score,
        "overall_risk": overall_risk,
        "reasons": reasons,
        "ai_explanation": explanation,
        "next_step": next_step,
        "reviewer_queue": reviewer_queue,
    }


def build_ai_explanation(
    site: dict[str, Any], overall_risk: str, reasons: list[str]
) -> str:
    """Create a concise AI-style explanation for planners and reviewers."""
    reason_text = ", ".join(reason.lower() for reason in reasons[:4])
    if len(reasons) > 4:
        reason_text += ", and additional proximity or vulnerability factors"

    review_guidance = (
        "The case should be routed to human review before a planning recommendation is finalized."
        if overall_risk in {"Medium", "High"}
        else "The case can receive an automatic low-risk recommendation, with optional planner review if local policy requires it."
    )

    return (
        f"This site is classified as {overall_risk.lower()} risk because it shows "
        f"{reason_text}. The result should be used as an early screening signal, "
        f"not as a final permitting decision. {review_guidance}"
    )


def screen_site(query: str, csv_path: str | Path = DEFAULT_CSV_PATH) -> dict[str, Any]:
    """Screen a planning site by matching it to the sample GIS dataset."""
    sites = load_sites(csv_path)
    site = find_site(query, sites)
    if site is None:
        return {
            "status": "error",
            "message": (
                "Site not found. Please check the address or add the site to the "
                "GIS screening dataset."
            ),
        }

    result = calculate_risk(site)
    result["status"] = "success"
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a GeoCase AI site screening.")
    parser.add_argument("query", nargs="?", help="Planning site name or address")
    parser.add_argument(
        "--csv",
        default=DEFAULT_CSV_PATH,
        help="Path to the sample GIS screening CSV",
    )
    args = parser.parse_args()

    query = args.query or input("Enter site name or address: ")
    result = screen_site(query, args.csv)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
