# GeoCase AI Deck Outline

## Slide 1: Title

GeoCase AI  
Agentic GIS Risk Screening for Urban Planning

## Slide 2: Problem

Urban planning teams must manually screen development sites across fragmented GIS, environmental, infrastructure, and demographic datasets.

## Slide 3: Solution

GeoCase AI uses UiPath to orchestrate case intake, GIS screening, AI explanation, human review, and report generation.

## Slide 4: UiPath-Orchestrated Workflow

User / Planner  
to UiPath Case Intake Form  
to UiPath Maestro Case  
to GeoCase AI API  
to GIS Risk Screening Agent  
to Risk-Based Routing  
to Human Review  
to Generated Report  
to Case Closed

Speaker note: This is not a standalone dashboard. The dashboard mirrors the same API calls used by UiPath.

## Slide 5: Agents

- Site Intake Agent
- GIS Risk Screening Agent
- Environmental Justice Agent
- Risk Explanation Agent
- Report Generation Agent
- Human Review Task

## Slide 6: Demo Case: High Risk

52nd St Station Redevelopment

- Risk level: High
- Risk score: 12
- Workflow path: Environmental Justice Review
- Human reviewer decision: Request additional environmental study

## Slide 7: Dynamic Routing

| Site | Risk | Workflow |
| --- | --- | --- |
| 52nd St Station | High | Environmental justice review |
| Manayunk | Medium | Planner review |
| City Hall | Low | Automatic recommendation |

## Slide 8: Responsible AI

AI supports early-stage review but does not replace qualified human planners or environmental justice reviewers. Medium- and high-risk cases require human-in-the-loop review.

## Slide 9: Production Path

Future integrations:

- FEMA flood maps
- Census ACS demographics
- NOAA rainfall data
- USGS data
- OpenStreetMap
- Local municipal GIS portals

## Slide 10: Impact

- Faster initial planning review
- More consistent screening
- Earlier environmental justice flags
- Clear audit trail
- Humans remain in control
