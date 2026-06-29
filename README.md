# GeoCase AI

**A UiPath-orchestrated agentic GIS case management workflow for urban planning and environmental review.**

GeoCase AI turns GIS risk screening into a case workflow: UiPath handles intake, case orchestration, routing, and human review, while the GeoCase AI API provides GIS risk screening, environmental justice reasoning, and report generation.

## AgentHack Positioning

GeoCase AI is not a GIS chatbot and not just a scoring dashboard. It is an agentic case review workflow where each proposed development site becomes a planning case.

```text
UiPath Case Intake
→ GeoCase AI API
→ GIS Risk Screening Agent
→ Environmental Justice Agent
→ Risk-Based Routing
→ Human Review
→ Report Generation
→ Case Closed
```

## Demo Flow

The recommended demo shows UiPath or the local dashboard calling the same API workflow:

1. Create a planning case for a proposed development site.
2. Call `POST /cases` to run GIS and environmental justice screening.
3. Route the case based on `screening_result.overall_risk`.
4. Send high-risk and medium-risk cases to human review.
5. Submit the reviewer decision through `POST /cases/{case_id}/review`.
6. Retrieve the final report through `GET /cases/{case_id}/report`.

## Demo Cases

| Case | Risk | Workflow purpose |
| --- | --- | --- |
| `52nd St Station` | High | Shows environmental justice human review |
| `Manayunk` | Medium | Shows planner review routing |
| `City Hall` | Low | Shows automatic recommendation |

These three cases prove that the workflow is not hard-coded to one outcome. The same process dynamically changes path based on GIS risk.

## UiPath Role

UiPath is the orchestration layer:

- Creates the planning case
- Sends the site information to GeoCase AI through HTTP Request
- Reads risk score, risk level, reasons, and recommended next step
- Routes the case to auto recommendation, planner review, or environmental justice review
- Keeps humans in the loop for medium- and high-risk cases
- Attaches or stores the final risk screening report

The local dashboard is a demo and fallback interface. It mirrors the same API calls used by UiPath. In the UiPath workflow, Automation Cloud acts as the orchestration layer while GeoCase AI provides the GIS screening and reporting service.

## What It Does

GeoCase AI screens proposed development sites for:

- Flood exposure
- Extreme rainfall exposure
- Noise exposure
- Environmental justice indicators
- Poverty and minority population indicators
- Proximity to schools
- Proximity to major transit infrastructure
- Proximity to rivers or waterways

The result includes:

- Case ID
- Case status
- Risk score
- Overall risk level
- Key reasons
- AI planning explanation
- Workflow path
- Human review task
- Markdown report

## Risk Routing

| Risk level | Case status | Workflow action |
| --- | --- | --- |
| Low | `Closed - Auto Recommendation Generated` | Generate automatic recommendation |
| Medium | `Awaiting Planner Review` | Route to planner review |
| High | `Awaiting Environmental Justice Review` | Route to environmental justice reviewer |

## Agents

1. Site Intake Agent: receives the planning site address and creates a case.
2. GIS Risk Screening Agent: matches the site to GIS indicators and scores flood, rainfall, noise, and proximity risk.
3. Environmental Justice Agent: evaluates demographic vulnerability and equity-related indicators.
4. Risk Explanation Agent: creates planner-readable reasoning.
5. Report Generation Agent: creates the final markdown screening report.
6. Human Review Task: keeps planners and environmental reviewers in control of medium- and high-risk cases.

## UiPath Components

- UiPath Automation Cloud
- UiPath Maestro Case
- HTTP Request or API workflow
- Human-in-the-loop review task
- GeoCase AI FastAPI service
- GeoCase AI Dashboard for local demo playback

## Run Locally

Install dependencies:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Start the local API and dashboard:

```bash
.venv/bin/uvicorn src.api:app --reload
```

Open:

```text
http://127.0.0.1:8000/dashboard
```

Run the command-line fallback demo:

```bash
.venv/bin/python src/app.py "52nd St Station"
```

## API Endpoints

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/dashboard` | Local demo dashboard |
| `GET` | `/screen?query=52nd%20St%20Station` | Standalone GIS screening |
| `POST` | `/cases` | Create planning case and run workflow |
| `GET` | `/cases` | List stored cases |
| `GET` | `/cases/{case_id}` | Get case detail |
| `POST` | `/cases/{case_id}/review` | Submit human reviewer decision |
| `GET` | `/cases/{case_id}/report` | Retrieve final markdown report |

Create a full planning case:

```bash
curl -X POST http://127.0.0.1:8000/cases \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "52nd St Station Redevelopment",
    "address": "52nd St Station",
    "project_type": "Transit-adjacent redevelopment",
    "reviewer": "Environmental Planning Team"
  }'
```

Submit a human review decision:

```bash
curl -X POST http://127.0.0.1:8000/cases/GEO-0001/review \
  -H "Content-Type: application/json" \
  -d '{
    "decision": "Request additional environmental study",
    "reviewer_name": "Environmental Planning Team",
    "notes": "Additional noise and environmental justice mitigation review required before recommendation."
  }'
```

Retrieve the final report:

```text
http://127.0.0.1:8000/cases/GEO-0001/report
```

## Prototype Data

The prototype uses `data/sample_sites.csv`, a small sample GIS screening dataset for Philadelphia demo sites. In production, the same workflow can connect to FEMA flood maps, Census ACS demographics, NOAA rainfall data, USGS data, OpenStreetMap, and local municipal open data portals.

## Submission Materials

- Devpost copy: `docs/devpost_description.md`
- Demo video script: `docs/demo_video_script.md`
- Deck outline: `docs/deck_outline.md`
- Architecture notes: `docs/architecture.md`
- Workflow diagram notes: `docs/workflow_diagram.md`
- UiPath workflow notes: `uipath/workflow_notes.md`
- UiPath HTTP payload examples: `uipath/http_payloads.json`

## Repository Structure

```text
geocase-ai/
├── README.md
├── LICENSE
├── requirements.txt
├── data/
│   ├── case_store.json
│   └── sample_sites.csv
├── src/
│   ├── api.py
│   ├── app.py
│   ├── case_workflow.py
│   ├── report_generator.py
│   └── risk_screening.py
├── reports/
│   ├── example_report.md
│   └── cases/
├── docs/
│   ├── architecture.png
│   ├── architecture.md
│   ├── deck_outline.md
│   ├── demo_video_script.md
│   ├── devpost_description.md
│   ├── workflow_diagram.png
│   └── workflow_diagram.md
└── uipath/
    ├── http_payloads.json
    └── workflow_notes.md
```

## Responsible Use

This prototype is intended to support early-stage planning review. AI-generated screening results should not be treated as final permitting decisions. Medium- and high-risk cases are intentionally routed to qualified human reviewers.

## License

MIT
