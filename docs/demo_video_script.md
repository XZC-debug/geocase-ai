# GeoCase AI Demo Video Script

## 0:00-0:30 Problem

Urban planning and environmental review teams often need to screen proposed development sites across flood exposure, extreme rainfall, noise, environmental justice indicators, schools, transit infrastructure, and waterways. Today this review is often manual, inconsistent, and spread across fragmented GIS systems.

## 0:30-1:00 Solution

GeoCase AI turns GIS risk screening into a UiPath-orchestrated case management workflow. UiPath acts as the orchestration layer for case intake, status, routing, human review, and reporting. GeoCase AI provides the GIS screening agent, environmental justice reasoning, and report service.

Key line to say:

```text
GeoCase AI is not a GIS chatbot. It is a UiPath-orchestrated GIS case review workflow.
```

## 1:00-2:00 High-Risk Case

Open the GeoCase AI Dashboard or UiPath intake form.

Enter:

- Project name: 52nd St Station Redevelopment
- Address: 52nd St Station
- Project type: Transit-adjacent redevelopment
- Reviewer: Environmental Planning Team

Click Start Screening.

Show:

- Case ID: `GEO-0001`
- Risk level: `High`
- Risk score: `12`
- Workflow path: `Environmental Justice Review`
- Status: `Awaiting Environmental Justice Review`
- Human review required: `true`

Explain that UiPath would receive these fields from `POST /cases` and route the case based on `screening_result.overall_risk`.

## 2:00-2:45 Human Review

Show the Human Review panel.

Select:

- Request additional environmental study

Add reviewer notes and submit.

Show the status changing to:

- `Human Review Completed`

Explain:

```text
High-risk cases do not close automatically. AI supports the decision, but a qualified human reviewer remains in control.
```

## 2:45-3:30 Report

Open the generated report preview.

Highlight:

- Site information
- GIS risk summary
- Key reasons
- AI planning explanation
- Recommended next step
- Responsible use note
- Human reviewer decision

Explain that UiPath can retrieve this report from:

```text
GET /cases/{case_id}/report
```

## 3:30-4:20 Dynamic Routing

Show the other two demo cases:

| Site | Risk | Workflow |
| --- | --- | --- |
| Manayunk | Medium | Planner Review |
| City Hall | Low | Automatic Recommendation |

Explain that the workflow is not hard-coded. The same case process takes different paths based on GIS risk.

## 4:20-5:00 Architecture and Impact

Show the architecture slide or README diagram:

```text
UiPath Case Intake
→ GeoCase AI API
→ GIS Risk Screening Agent
→ Risk-Based Routing
→ Human Review
→ Report Generation
```

Closing line:

```text
GeoCase AI demonstrates how UiPath can orchestrate AI agents, GIS risk screening, human review, and report generation for urban planning case review.
```

Mention future production integrations:

- FEMA flood maps
- Census ACS demographics
- NOAA rainfall data
- USGS data
- OpenStreetMap
- Local municipal open data portals
