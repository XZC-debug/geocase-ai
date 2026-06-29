# GeoCase AI: Agentic GIS Risk Screening for Urban Planning

## Tagline

A UiPath-orchestrated AI case management workflow that screens urban planning sites for environmental, flood, rainfall, noise, and equity risks.

## Inspiration

Urban planning and environmental review teams often need to evaluate proposed development sites using fragmented geospatial datasets. This process can be slow, inconsistent, and difficult to scale. GeoCase AI was inspired by the need for faster, more transparent, and human-centered GIS risk screening.

## What It Does

GeoCase AI takes a planning site as input, creates a planning case, screens it against GIS risk indicators, generates an AI-assisted risk explanation, and routes the case based on its risk level. Low-risk cases receive an automatic recommendation, medium-risk cases go to planner review, and high-risk cases go to environmental justice review. The local dashboard demonstrates the same case lifecycle that UiPath can orchestrate through HTTP requests.

The main demo cases are:

- 52nd St Station: high risk, routed to environmental justice review.
- Manayunk: medium risk, routed to planner review.
- City Hall: low risk, closed with an automatic recommendation.

## How We Built It

We built the prototype around UiPath Automation Cloud and Maestro Case as the orchestration layer. A Python-based FastAPI service evaluates sample site data for flood exposure, rainfall exposure, noise exposure, environmental justice indicators, and proximity to sensitive facilities. The service also exposes case workflow endpoints for case creation, risk-based routing, human review submission, and report retrieval. UiPath can coordinate the case flow, invoke the screening API, route high-risk cases to human review, and support final report generation.

## UiPath Role

UiPath is the case orchestration layer. It creates the planning case, sends the site address to the GeoCase AI screening service, receives the risk JSON, applies routing logic, creates a human review task when needed, and closes the case after the final report is generated.

The dashboard is included for local demo playback and mirrors the same API calls used by UiPath: `POST /cases`, `POST /cases/{case_id}/review`, and `GET /cases/{case_id}/report`.

## AI and Agents

- Site Intake Agent parses the planning site input.
- GIS Risk Screening Agent evaluates risk indicators.
- Environmental Justice Agent flags equity-sensitive conditions.
- Report Generation Agent produces the screening report.
- Human Review Task keeps planners and reviewers in control of medium- and high-risk cases.

## Challenges

The main challenge was translating GIS risk analysis into an agentic workflow that is understandable, auditable, and appropriate for human review. We designed the system so that AI supports planning judgment rather than replacing it.

## Accomplishments

- Built a working Python screening service.
- Built a local dashboard for end-to-end case review demos.
- Added case workflow API endpoints for UiPath HTTP Request integration.
- Created a sample GIS risk dataset for demo cases.
- Implemented deterministic risk scoring and routing.
- Generated one-page markdown reports with human reviewer decisions.
- Documented how UiPath can orchestrate the end-to-end case workflow.

## What Is Next

Future versions can connect to live FEMA flood maps, Census ACS demographics, NOAA rainfall data, USGS elevation data, OpenStreetMap, and local municipal open data portals. The human review screen can also be extended with mitigation options, reviewer notes, and final approval history.
