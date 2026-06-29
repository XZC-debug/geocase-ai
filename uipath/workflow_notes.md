# UiPath Workflow Notes

## Recommended Track

Track 1: UiPath Maestro Case

GeoCase AI fits the case model because each development site is a separate planning review case. Different sites may require different paths, including automatic recommendation, planner review, environmental justice review, or exception handling for missing data.

## Strong Demo Case Flow

1. Case Intake Form captures project name, address, project type, and reviewer team.
2. UiPath creates a Planning Site Review case.
3. UiPath calls the GeoCase AI Case API.
4. GeoCase AI creates a `GEO-0001` style case ID.
5. GeoCase AI runs GIS screening and environmental justice screening.
6. GeoCase AI returns risk score, reasons, AI explanation, workflow path, status, and report path.
7. UiPath branches on `screening_result.overall_risk`.
8. Low risk cases receive an automatic low-risk recommendation and close.
9. Medium risk cases create a planner review task.
10. High risk cases create an environmental justice review task.
11. Reviewer submits decision and notes.
12. GeoCase AI updates the case status and regenerates the report.
13. UiPath attaches or links the final report and closes the case.

## Run the Local API

```bash
uvicorn src.api:app --reload
```

Open the dashboard:

```text
http://127.0.0.1:8000/dashboard
```

## Create Case HTTP Request

Use this request from UiPath HTTP Request:

```text
POST http://127.0.0.1:8000/cases
Content-Type: application/json
```

Body:

```json
{
  "project_name": "52nd St Station Redevelopment",
  "address": "52nd St Station",
  "project_type": "Transit-adjacent redevelopment",
  "reviewer": "Environmental Planning Team"
}
```

Key response fields:

- `case_id`
- `case_name`
- `status`
- `workflow_path`
- `human_review_required`
- `human_review_task`
- `case_decision`
- `report_path`
- `screening_result.overall_risk`
- `screening_result.risk_score`
- `screening_result.reasons`
- `screening_result.ai_explanation`
- `screening_result.next_step`

## Routing Logic

| Risk level | Case status | UiPath action |
| --- | --- | --- |
| Low | Closed - Auto Recommendation Generated | Close with automatic recommendation |
| Medium | Awaiting Planner Review | Create planner review task |
| High | Awaiting Environmental Justice Review | Create environmental justice reviewer task |

## Human Review Task

Recommended task title:

```text
GeoCase AI Human Review: {{case_id}} - {{case_name}}
```

Recommended fields:

- Case ID
- Case name
- Site address
- Project type
- Overall risk level
- Risk score
- Key reasons
- AI planning explanation
- Recommended next step
- Reviewer decision
- Reviewer notes

Recommended reviewer decisions:

- Approve with mitigation
- Request additional environmental study
- Escalate to senior reviewer
- Reject recommendation

## Submit Review HTTP Request

After the reviewer completes the task, call:

```text
POST http://127.0.0.1:8000/cases/GEO-0001/review
Content-Type: application/json
```

Body:

```json
{
  "decision": "Request additional environmental study",
  "reviewer_name": "Environmental Planning Team",
  "notes": "Additional environmental study requested before recommendation."
}
```

Expected response:

- `status`: `Human Review Completed`
- `case_decision`: reviewer decision
- `human_review.decision`
- `human_review.notes`
- updated `report_path`

## Report Request

```text
GET http://127.0.0.1:8000/cases/GEO-0001/report
```

UiPath can attach the markdown text to the case, write it to a file, or include it in a final notification.

## Demo Cases

Use three sample cases to show dynamic routing:

| Input | Expected risk | Workflow |
| --- | --- | --- |
| `52nd St Station` | High | Environmental justice review |
| `Manayunk` | Medium | Planner review |
| `City Hall` | Low | Automatic recommendation |

## Fallback Option

If UiPath HTTP integration is not ready in time, use the local dashboard for the video and explain that the dashboard mirrors the same API calls UiPath uses:

- `POST /cases`
- `POST /cases/{case_id}/review`
- `GET /cases/{case_id}/report`

## Production Data Path

The prototype uses a sample GIS risk dataset. A production version can replace the CSV with FEMA, Census ACS, NOAA, USGS, OpenStreetMap, and local open data APIs while keeping the same UiPath case flow.
