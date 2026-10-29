# Reproduction Guide

This guide explains how to reproduce the baseline and advanced AI Data Quality & Research Agent from a clean Windows environment.

## Requirements

* Windows 10/11
* Python 3.12+
* Internet connection for package installation and OpenAI API access
* OpenAI API key

## 1. Create and activate the virtual environment

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell activation is restricted, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

## 2. Install dependencies

```powershell
pip install -r requirements.txt
```

## 3. Configure the API key

Copy `.env.example` to `.env`:

```powershell
copy .env.example .env
```

Open `.env` and add your own OpenAI API key:

```text
OPENAI_API_KEY=your_api_key_here
```

Never commit or submit `.env`. The API key must remain local.

## 4. Run the application

From the project root:

```powershell
streamlit run app/main.py
```

Alternatively, on Windows the included launcher can be used:

```bat
run_app.bat
```

The application opens at:

```text
http://localhost:8501
```

Upload a CSV or XLSX dataset through the Streamlit interface.

## 5. Run the baseline

The baseline provides the initial deterministic missing-value and duplicate-row checks.

```powershell
python baseline/baseline.py sample_data/demo_customers.csv
```

The baseline output provides the starting point for comparison with the advanced workflow.

## 6. Run evaluation

Generate the fixed evaluation cases:

```powershell
python evaluation/generate_cases.py
```

Run the evaluator:

```powershell
python evaluation/evaluate.py
```

Evaluation output is used to compare deterministic data-quality coverage and workflow behavior.

## 7. Run automated tests

```powershell
pytest -q --cov=app --cov=baseline
```

The test suite validates core application and baseline behavior.

## 8. Expected workflow

The advanced solution follows this pipeline:

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

Deterministic Python checks perform the measurable data-quality calculations. Agents interpret semantic findings, research contextual questions when useful, verify findings, and generate the final report.

## 9. Expected outputs

The application can produce:

```text
Quality profile
Data-quality findings
Agent research findings
Verification result
Decision-ready report
Agent trajectory JSON
Evaluation JSON
```

Representative agent trajectories are stored under:

```text
trajectories/
```

## 10. Runtime and cost

Runtime depends on dataset size, number of findings, network conditions, and model/API response time.

Deterministic analysis is local and normally completes quickly for the included sample datasets. Agentic research and report generation require OpenAI API access and therefore may incur API usage costs according to the selected model and current OpenAI pricing.

No fixed cost is assumed by this project because usage depends on the dataset and number of agent calls.

## 11. Reproducibility and safety

* Use synthetic or permitted datasets for testing.
* Keep API credentials outside the repository.
* Review findings before making irreversible data corrections.
* Statistical anomalies are not automatically treated as errors.
* Agent trajectories provide evidence of the research and verification workflow.

## Design Principle

**Compute deterministically. Research when necessary. Verify skeptically. Report with evidence.**
