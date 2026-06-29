"""Interactive command-line demo for GeoCase AI."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from .report_generator import generate_report
    from .risk_screening import PROJECT_ROOT, screen_site
except ImportError:
    from report_generator import generate_report
    from risk_screening import PROJECT_ROOT, screen_site


def run_demo(query: str, output_path: Path) -> dict:
    result = screen_site(query)
    report = generate_report(result)
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="GeoCase AI: Agentic GIS Risk Screening"
    )
    parser.add_argument("query", nargs="?", help="Planning site name or address")
    parser.add_argument(
        "--report",
        default=PROJECT_ROOT / "reports" / "latest_report.md",
        type=Path,
        help="Path for the generated markdown report",
    )
    args = parser.parse_args()

    print("GeoCase AI: Agentic GIS Risk Screening")
    print("--------------------------------------")
    query = args.query or input("Enter planning site name or address: ")

    result = run_demo(query, args.report)
    print("\nScreening Result:")
    print(json.dumps(result, indent=2))
    print(f"\nReport saved to: {args.report}")


if __name__ == "__main__":
    main()
