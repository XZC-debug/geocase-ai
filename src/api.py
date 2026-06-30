"""FastAPI service and dashboard for UiPath or demo integrations."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse
from pydantic import BaseModel

from .case_workflow import (
    create_case,
    get_case,
    list_cases,
    submit_human_review,
)
from .report_generator import generate_case_report, generate_report
from .risk_screening import screen_site


app = FastAPI(
    title="GeoCase AI API",
    description="Agentic GIS risk screening API for UiPath planning case review.",
    version="0.2.0",
)


class ScreenRequest(BaseModel):
    query: str


class CaseCreateRequest(BaseModel):
    project_name: str
    address: str
    project_type: str
    reviewer: str


class HumanReviewRequest(BaseModel):
    decision: str
    notes: str = ""
    reviewer_name: str


@app.get("/", include_in_schema=False)
def home() -> RedirectResponse:
    return RedirectResponse(url="/dashboard")


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard() -> str:
    return DASHBOARD_HTML


@app.get("/screen")
def screen(query: str) -> dict:
    return screen_site(query)


@app.post("/screen")
def screen_post(request: ScreenRequest) -> dict:
    return screen_site(request.query)


@app.get("/report")
def report(query: str) -> dict[str, str]:
    result = screen_site(query)
    markdown_report = generate_report(result)
    return {
        "query": query,
        "status": result["status"],
        "report": markdown_report,
    }


@app.post("/cases")
def create_planning_case(request: CaseCreateRequest) -> dict:
    return create_case(
        project_name=request.project_name,
        address=request.address,
        project_type=request.project_type,
        reviewer=request.reviewer,
    )


@app.get("/cases")
def get_cases() -> list[dict]:
    return list_cases()


@app.get("/cases/{case_id}")
def get_planning_case(case_id: str) -> dict:
    case = get_case(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@app.post("/cases/{case_id}/review")
def review_case(case_id: str, request: HumanReviewRequest) -> dict:
    try:
        case = submit_human_review(
            case_id=case_id,
            decision=request.decision,
            notes=request.notes,
            reviewer_name=request.reviewer_name,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@app.get("/cases/{case_id}/report", response_class=PlainTextResponse)
def get_case_report(case_id: str) -> str:
    case = get_case(case_id)
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    report_path = case.get("report_path")
    if report_path and Path(report_path).exists():
        return Path(report_path).read_text(encoding="utf-8")
    return generate_case_report(case)


DASHBOARD_HTML = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>GeoCase AI Dashboard</title>
  <style>
    :root {
      color-scheme: light;
      --ink: #17202a;
      --muted: #5f6b7a;
      --line: #d8dee8;
      --panel: #ffffff;
      --soft: #f6f8fb;
      --accent: #146c94;
      --accent-2: #2e7d58;
      --warn: #a65f00;
      --danger: #a83246;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--soft);
      color: var(--ink);
    }
    header {
      padding: 28px 34px 22px;
      background: #ffffff;
      border-bottom: 1px solid var(--line);
    }
    h1 { margin: 0; font-size: 28px; letter-spacing: 0; }
    header p { margin: 8px 0 0; color: var(--muted); max-width: 860px; }
    main {
      display: grid;
      grid-template-columns: 390px 1fr;
      gap: 18px;
      padding: 18px;
    }
    section {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 18px;
    }
    h2 { margin: 0 0 14px; font-size: 18px; }
    label {
      display: block;
      margin: 12px 0 6px;
      color: #344054;
      font-size: 13px;
      font-weight: 650;
    }
    input, select, textarea {
      width: 100%;
      border: 1px solid #c7d0dd;
      border-radius: 6px;
      padding: 10px 11px;
      font: inherit;
      background: #ffffff;
      color: var(--ink);
    }
    textarea { min-height: 86px; resize: vertical; }
    button {
      border: 0;
      border-radius: 6px;
      padding: 10px 13px;
      font: inherit;
      font-weight: 700;
      color: #ffffff;
      background: var(--accent);
      cursor: pointer;
    }
    button.secondary { background: #475467; }
    button:disabled { opacity: .55; cursor: not-allowed; }
    .button-row { display: flex; gap: 10px; margin-top: 16px; flex-wrap: wrap; }
    .content-grid {
      display: grid;
      grid-template-columns: minmax(0, 1.1fr) minmax(320px, .9fr);
      gap: 18px;
    }
    .case-list {
      display: grid;
      gap: 10px;
      max-height: 420px;
      overflow: auto;
    }
    .case-item {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      cursor: pointer;
      background: #ffffff;
    }
    .case-item:hover { border-color: var(--accent); }
    .case-title { font-weight: 800; }
    .muted { color: var(--muted); font-size: 13px; }
    .pill {
      display: inline-block;
      padding: 4px 8px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 800;
      margin: 6px 6px 0 0;
      background: #eef2f7;
    }
    .risk-Low { color: #146c43; background: #e7f5ed; }
    .risk-Medium { color: #8a4b00; background: #fff1d6; }
    .risk-High { color: #9b1c31; background: #fde7ed; }
    .status { color: #1d4f72; background: #e7f1f8; }
    .timeline {
      display: grid;
      grid-template-columns: repeat(5, minmax(120px, 1fr));
      gap: 8px;
      margin-bottom: 16px;
    }
    .step {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 10px;
      min-height: 72px;
      background: #fafbfc;
    }
    .step strong { display: block; font-size: 13px; }
    .step.done { border-color: #7bb699; background: #edf8f2; }
    .step.active { border-color: #146c94; background: #e8f3f8; }
    .detail {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      background: #ffffff;
    }
    ul { margin: 8px 0 0; padding-left: 20px; }
    pre {
      white-space: pre-wrap;
      max-height: 360px;
      overflow: auto;
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      background: #f8fafc;
      font-size: 13px;
    }
    @media (max-width: 980px) {
      main, .content-grid { grid-template-columns: 1fr; }
      .timeline { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <header>
    <h1>GeoCase AI Dashboard</h1>
    <p>UiPath-compatible GIS case review workflow: this dashboard mirrors the same API calls UiPath uses for intake, case creation, GIS screening, risk-based routing, human review, and report generation.</p>
  </header>
  <main>
    <section>
      <h2>Start Screening</h2>
      <label for="projectName">Project name</label>
      <input id="projectName" value="52nd St Station Redevelopment">
      <label for="address">Address or site query</label>
      <input id="address" value="52nd St Station">
      <label for="projectType">Project type</label>
      <input id="projectType" value="Transit-adjacent redevelopment">
      <label for="reviewer">Reviewer team</label>
      <input id="reviewer" value="Environmental Planning Team">
      <div class="button-row">
        <button onclick="startCase()">Start Screening</button>
        <button class="secondary" onclick="loadDemoCases()">Load Demo Cases</button>
      </div>
      <h2 style="margin-top: 24px;">Cases</h2>
      <div id="caseList" class="case-list"></div>
    </section>
    <div class="content-grid">
      <section>
        <h2>Case Flow</h2>
        <div class="timeline" id="timeline"></div>
        <div id="caseDetail" class="detail">Select or create a case to view the workflow.</div>
      </section>
      <section>
        <h2>Human Review</h2>
        <div id="reviewPanel" class="detail">A review task appears here for medium- and high-risk cases.</div>
        <h2 style="margin-top: 18px;">Report</h2>
        <pre id="reportPreview">No report selected.</pre>
      </section>
    </div>
  </main>
  <script>
    let selectedCase = null;

    const workflowSteps = [
      "Case Created",
      "GIS Screening",
      "Risk Routing",
      "Human Review",
      "Report Saved"
    ];

    async function api(path, options = {}) {
      const response = await fetch(path, {
        headers: { "Content-Type": "application/json" },
        ...options
      });
      if (!response.ok) {
        const text = await response.text();
        throw new Error(text);
      }
      const contentType = response.headers.get("content-type") || "";
      return contentType.includes("application/json") ? response.json() : response.text();
    }

    async function startCase() {
      const body = {
        project_name: document.getElementById("projectName").value,
        address: document.getElementById("address").value,
        project_type: document.getElementById("projectType").value,
        reviewer: document.getElementById("reviewer").value
      };
      selectedCase = await api("/cases", { method: "POST", body: JSON.stringify(body) });
      await refreshCases();
      renderCase(selectedCase);
    }

    async function loadDemoCases() {
      const demos = [
        ["52nd St Station Redevelopment", "52nd St Station", "Transit-adjacent redevelopment", "Environmental Planning Team"],
        ["Manayunk Hillside Housing", "Manayunk", "Hillside residential development", "Planning Review Team"],
        ["City Hall Renovation", "City Hall", "Commercial renovation", "Planning Review Team"]
      ];
      for (const [project_name, address, project_type, reviewer] of demos) {
        await api("/cases", { method: "POST", body: JSON.stringify({ project_name, address, project_type, reviewer }) });
      }
      await refreshCases();
    }

    async function refreshCases() {
      const cases = await api("/cases");
      const list = document.getElementById("caseList");
      list.innerHTML = "";
      cases.slice().reverse().forEach(item => {
        const risk = item.screening_result.overall_risk || "Exception";
        const div = document.createElement("div");
        div.className = "case-item";
        div.onclick = () => renderCase(item);
        div.innerHTML = `
          <div class="case-title">${item.case_id} · ${item.case_name}</div>
          <div class="muted">${item.address}</div>
          <span class="pill risk-${risk}">${risk}</span>
          <span class="pill status">${item.status}</span>
        `;
        list.appendChild(div);
      });
    }

    function renderTimeline(item) {
      const risk = item.screening_result.overall_risk;
      const reviewDone = Boolean(item.human_review);
      const autoClosed = risk === "Low";
      const activeIndex = reviewDone || autoClosed ? 4 : item.human_review_required ? 3 : 2;
      document.getElementById("timeline").innerHTML = workflowSteps.map((step, index) => {
        const klass = index < activeIndex ? "done" : index === activeIndex ? "active" : "";
        return `<div class="step ${klass}"><strong>${step}</strong><span class="muted">${stepText(item, index)}</span></div>`;
      }).join("");
    }

    function stepText(item, index) {
      const result = item.screening_result;
      return [
        item.case_id,
        result.status === "success" ? "GIS agent returned risk data" : "Address match failed",
        item.workflow_path,
        item.human_review_required ? (item.human_review ? item.human_review.decision : "Decision required") : "Not required",
        item.report_path || "Pending"
      ][index];
    }

    async function renderCase(item) {
      selectedCase = item;
      renderTimeline(item);
      const result = item.screening_result;
      const reasons = (result.reasons || []).map(reason => `<li>${reason}</li>`).join("");
      document.getElementById("caseDetail").innerHTML = `
        <h2>${item.case_id}: ${item.case_name}</h2>
        <p><span class="pill risk-${result.overall_risk}">${result.overall_risk || "Exception"}</span><span class="pill status">${item.status}</span></p>
        <p><strong>Workflow path:</strong> ${item.workflow_path}</p>
        <p><strong>Risk score:</strong> ${result.risk_score ?? "N/A"}</p>
        <p><strong>Next step:</strong> ${result.next_step || item.case_decision}</p>
        <p><strong>AI explanation:</strong> ${result.ai_explanation || result.message}</p>
        <strong>Key reasons</strong>
        <ul>${reasons}</ul>
      `;
      renderReview(item);
      await loadReport(item.case_id);
    }

    function renderReview(item) {
      const panel = document.getElementById("reviewPanel");
      if (!item.human_review_required) {
        panel.innerHTML = `<p><strong>No manual review required.</strong></p><p>${item.case_decision}</p>`;
        return;
      }
      if (item.human_review) {
        panel.innerHTML = `
          <p><strong>Decision:</strong> ${item.human_review.decision}</p>
          <p><strong>Reviewer:</strong> ${item.human_review.reviewer_name}</p>
          <p><strong>Notes:</strong> ${item.human_review.notes || "No notes provided"}</p>
        `;
        return;
      }
      panel.innerHTML = `
        <label for="decision">Reviewer decision</label>
        <select id="decision">
          <option>Request additional environmental study</option>
          <option>Approve with mitigation</option>
          <option>Escalate to senior reviewer</option>
          <option>Reject recommendation</option>
        </select>
        <label for="reviewerName">Reviewer name</label>
        <input id="reviewerName" value="${item.reviewer}">
        <label for="notes">Reviewer notes</label>
        <textarea id="notes">Additional environmental study requested before recommendation.</textarea>
        <div class="button-row"><button onclick="submitReview()">Submit Human Review</button></div>
      `;
    }

    async function submitReview() {
      if (!selectedCase) return;
      selectedCase = await api(`/cases/${selectedCase.case_id}/review`, {
        method: "POST",
        body: JSON.stringify({
          decision: document.getElementById("decision").value,
          reviewer_name: document.getElementById("reviewerName").value,
          notes: document.getElementById("notes").value
        })
      });
      await refreshCases();
      renderCase(selectedCase);
    }

    async function loadReport(caseId) {
      document.getElementById("reportPreview").textContent = await api(`/cases/${caseId}/report`);
    }

    refreshCases();
  </script>
</body>
</html>
"""
