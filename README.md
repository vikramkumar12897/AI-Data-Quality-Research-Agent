# AI Data Quality & Research Agent

An evidence-first agentic workflow designed for Data Analysts and Research Analysts to detect, investigate, verify, and communicate data-quality issues in CSV/XLSX datasets.

## Problem

Manual data-quality review can be slow and inconsistent. While basic issues such as missing values and duplicate records are easy to identify, real-world datasets also contain semantic inconsistencies, conflicting fields, unusual values, and ambiguous anomalies that require contextual investigation.

## Solution

The **AI Data Quality & Research Agent** combines deterministic data-quality checks with an agentic research and verification workflow.

The system separates objective computation from AI interpretation:

* **Python-based deterministic checks** identify measurable quality issues.
* **Research Agent** investigates semantic and contextual findings when additional evidence is useful.
* **Verification Agent** acts as a skeptical second reviewer and evaluates the evidence.
* **Report Generator** produces a concise, decision-ready report with recommendations and uncertainty.

## Workflow

```text
CSV/XLSX Dataset
      |
      v
Dataset Profiler
      |
      v
Deterministic Quality Analyzer
      |
      v
Research Agent
      |
      v
Verification Agent
      |
      v
Report Generator
      |
      v
Decision-Ready Report
```

## Data Quality Checks

The deterministic analysis currently covers:

* Missing values and completeness
* Duplicate records and uniqueness
* Numeric outliers using the IQR method
* Invalid date values
* Category inconsistencies and common aliases
* Cross-column consistency conflicts
* Overall quality scoring

The system does not automatically assume that every statistical anomaly is an error. Findings are surfaced for contextual review.

## Agent Roles

### Research Agent

Investigates findings that may benefit from semantic or contextual reasoning.

Capabilities include:

* Interpreting potentially equivalent category labels
* Explaining why a finding may represent a quality issue
* Assigning confidence
* Using public web evidence when it adds credible context
* Avoiding fabricated sources

### Verification Agent

Provides an independent, skeptical review of the detected findings.

It can:

* Accept supported findings
* Reject unsupported findings
* Downgrade ambiguous findings
* Provide reviewer notes
* Preserve uncertainty instead of treating every anomaly as an error

### Report Generator

Converts the verified analysis into a professional report containing:

* Executive summary
* Risk level
* Recommendations
* Research notes
* Evidence-grounded conclusions

## Key Features

* CSV and XLSX dataset upload
* Automated dataset profiling
* Deterministic data-quality analysis
* Agentic semantic research
* Evidence-based verification
* Risk-level assessment
* Downloadable Markdown report
* Downloadable findings JSON
* Agent trajectory logging for reproducibility

## Technology Stack

* Python
* Pandas
* NumPy
* Pydantic
* Streamlit
* OpenAI Agents SDK
* OpenAI API
* Web Search
* pytest

## Running the Application

Create and activate the virtual environment, install the dependencies, configure the API key locally, and start the Streamlit application.

See `REPRODUCTION.md` for the clean-environment setup and execution instructions.

The API key is stored locally through `.env` and should **never be included in the submission ZIP**.

## Example Dataset

A sample dataset is provided in:

```text
sample_data/
```

Upload a CSV or XLSX file through the Streamlit interface to begin the workflow.

## Outputs

The application can generate:

```text
data_quality_report.md
findings.json
trajectories/
```

The trajectory files provide a record of the agent workflow execution and support reproducibility and evaluation.

## Project Structure

```text
ai-data-quality-research-agent/
|
├── app/                  # Application and agent workflow
├── baseline/             # Baseline implementation
├── docs/                 # Project documentation
├── evaluation/           # Evaluation cases and evaluator
├── reference_data/       # Reference data
├── sample_data/          # Demo datasets
├── tests/                # Automated tests
├── trajectories/         # Agent execution trajectories
|
├── README.md
├── REPRODUCTION.md
├── CHANGELOG.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Hackathon Evidence

The repository includes supporting material for evaluation and reproducibility:

* `CHANGELOG.md` — development and improvement history
* `REPRODUCTION.md` — clean-environment setup guide
* `evaluation/` — fixed evaluation cases and evaluator
* `trajectories/` — representative agent workflow runs
* `tests/` — automated tests

## Design Principle

> **Compute deterministically. Research when necessary. Verify skeptically. Report with evidence.**

The goal is not simply to detect more anomalies, but to help analysts distinguish measurable data-quality problems from findings that require business-context validation.
