from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from app.models.schemas import (
    AgentReport,
    ResearchFinding,
    ResearchSource,
    VerificationResult,
)


def run_agentic_workflow(profile, findings, output_dir="trajectories"):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    log = {
        "run_id": run_id,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "agents": [],
    }

    # ---------------------------------------------------------
    # 1. RESEARCH AGENT
    # ---------------------------------------------------------
    research = []

    candidates = [
        f
        for f in findings
        if f.get("category") in {
            "Consistency",
            "Cross-column consistency",
        }
        or f.get("severity") != "critical"
    ]

    for finding in candidates:
        issue_id = finding.get("issue_id", "unknown")
        column = finding.get("column") or "dataset"
        message = finding.get("message", "")
        category = finding.get("category", "")

        normalized_value = str(
            finding.get("evidence", {}).get(
                "canonical_candidate",
                finding.get("evidence", {}).get("variants", column),
            )
        )

        interpretation = (
            f"The finding relates to {category.lower()} in '{column}'. "
            f"{message} "
            "The issue should be reviewed in the context of the dataset's "
            "business rules before corrective action is taken."
        )

        research.append(
            ResearchFinding(
                finding_id=issue_id,
                normalized_value=normalized_value,
                interpretation=interpretation,
                confidence=float(
                    finding.get("confidence", 0.80)
                ),
                sources=[
                    ResearchSource(
                        title="Internal deterministic data-quality evidence",
                        url="local://data-quality-check",
                    )
                ],
            )
        )

    log["agents"].append(
        {
            "name": "Research Agent",
            "instruction_summary": (
                "Semantic interpretation using deterministic dataset evidence"
            ),
            "tooling": [],
            "output": [x.model_dump() for x in research],
        }
    )

    # ---------------------------------------------------------
    # 2. VERIFICATION AGENT
    # ---------------------------------------------------------
    accepted = []
    rejected = []
    downgraded = []
    reviewer_notes = []

    for finding in findings:
        issue_id = finding.get("issue_id")
        severity = str(finding.get("severity", "")).lower()
        confidence = float(finding.get("confidence", 0))

        if severity == "critical":
            accepted.append(issue_id)
            reviewer_notes.append(
                f"{issue_id}: accepted because it is classified as critical."
            )

        elif confidence >= 0.85:
            accepted.append(issue_id)
            reviewer_notes.append(
                f"{issue_id}: accepted with confidence {confidence:.2f}."
            )

        elif confidence >= 0.70:
            downgraded.append(issue_id)
            reviewer_notes.append(
                f"{issue_id}: downgraded because the evidence requires "
                "additional business-context verification."
            )

        else:
            rejected.append(issue_id)
            reviewer_notes.append(
                f"{issue_id}: rejected because confidence is below the "
                "acceptance threshold."
            )

    verification = VerificationResult(
        accepted_finding_ids=accepted,
        rejected_finding_ids=rejected,
        downgraded_finding_ids=downgraded,
        reviewer_notes=reviewer_notes,
    )

    log["agents"].append(
        {
            "name": "Verification Agent",
            "instruction_summary": (
                "Skeptical evidence review and confidence control"
            ),
            "tooling": [],
            "output": verification.model_dump(),
        }
    )

    # ---------------------------------------------------------
    # 3. REPORT GENERATOR
    # ---------------------------------------------------------
    critical_count = sum(
        1 for f in findings
        if str(f.get("severity", "")).lower() == "critical"
    )

    warning_count = sum(
        1 for f in findings
        if str(f.get("severity", "")).lower() == "warning"
    )

    if critical_count > 0:
        risk_level = "High"
    elif warning_count >= 3:
        risk_level = "Medium"
    elif warning_count > 0:
        risk_level = "Low"
    else:
        risk_level = "Minimal"

    if not findings:
        executive_summary = (
            "The dataset passed the available deterministic data-quality "
            "checks. No material issues were identified by the current "
            "validation rules."
        )
    else:
        executive_summary = (
            f"The dataset contains {len(findings)} detected data-quality "
            f"finding(s), including {critical_count} critical and "
            f"{warning_count} warning-level issue(s). "
            f"The overall assessed risk level is {risk_level}. "
            "Findings should be reviewed against business rules before "
            "making irreversible data corrections."
        )

    recommendations = []

    for finding in findings:
        recommendation = finding.get("recommendation")

        if recommendation and recommendation not in recommendations:
            recommendations.append(recommendation)

    if not recommendations:
        recommendations.append(
            "Continue monitoring data quality using the available validation checks."
        )

    research_notes = [
        f"{x.finding_id}: {x.interpretation}"
        for x in research
    ]

    report = AgentReport(
        executive_summary=executive_summary,
        risk_level=risk_level,
        recommendations=recommendations,
        research_notes=research_notes,
    )

    log["agents"].append(
        {
            "name": "Report Generator",
            "instruction_summary": (
                "Decision-ready report synthesis from verified evidence"
            ),
            "tooling": [],
            "output": report.model_dump(),
        }
    )

    # ---------------------------------------------------------
    # SAVE TRAJECTORY
    # ---------------------------------------------------------
    out = output_dir / f"trajectory_{run_id}.json"

    out.write_text(
        json.dumps(
            log,
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    return {
        "research": research,
        "verification": verification,
        "report": report,
        "trajectory_path": str(out),
    }