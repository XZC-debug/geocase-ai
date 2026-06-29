# GeoCase AI Architecture

```mermaid
flowchart LR
    User["Planner or Intake User"] --> Maestro["UiPath Maestro Case"]
    Maestro --> Intake["Site Intake Agent"]
    Intake --> API["GeoCase AI API"]
    API --> Data["Sample GIS Risk Dataset"]
    API --> GIS["GIS Risk Screening Agent"]
    API --> EJ["Environmental Justice Agent"]
    GIS --> Scoring["Risk Score and Routing Decision"]
    EJ --> Scoring
    Scoring --> Report["Report Generation Agent"]
    Scoring --> Human["Human Review Task"]
    Human --> Maestro
    Report --> Maestro
    Maestro --> Result["Saved Case Result"]
```

UiPath coordinates the case lifecycle. The Python service provides GIS-style risk screening, risk explanation, and report content. Medium- and high-risk cases remain human-in-the-loop.
