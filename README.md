# PowerMind AI - Distribution Network Risk & Loss Intelligence System

PowerMind AI is a utility-focused analytics and Generative-AI application for distribution companies (DISCOs), with practical relevance for Pakistan's high-loss, high-growth urban feeders.

## Problem Statement (Pakistan DISCO Context)

DISCO engineers routinely manage overloaded feeders, thermal stress, and demand growth with limited decision-support tooling. This creates avoidable technical losses, voltage quality issues, and reliability risks. PowerMind AI addresses this by combining:

- Deterministic engineering risk scoring for each feeder
- Structured risk categorization (Low/Medium/High)
- Gemini-generated technical narratives for utility operations teams

The result is faster, more defensible feeder-level planning and intervention decisions.

## System Architecture

```text
CSV Input (uploaded or default synthetic dataset)
        |
        v
core/risk_engine.py (deterministic scoring + classification + engineering action)
        |
        v
Streamlit Dashboard (risk table, color-coded indicators, feeder drill-down)
        |
        v
core/ai_report.py (Gemini API for technical report generation)
```

Project structure:

```text
PowerMind-AI/
+-- app.py
+-- data/
¦   +-- transformer_data.csv
+-- core/
¦   +-- risk_engine.py
¦   +-- ai_report.py
¦   +-- data_generator.py
+-- requirements.txt
+-- README.md
```

## How Generative AI Is Used

Generative AI is used only in `core/ai_report.py`.

For a selected feeder, Gemini receives:

- Feeder operating metrics
- Computed risk score and risk level
- Deterministic engineering action

Gemini returns a formal technical report containing:

1. Technical situation summary
2. Root cause reasoning
3. Recommended utility actions

This keeps scoring deterministic while using Gen-AI for narrative and decision support.

## Setup and Run (uv)

1. Install dependencies:

```bash
uv pip install -r requirements.txt
```

2. Set environment variable for Gemini:

Windows PowerShell:

```powershell
$env:GEMINI_API_KEY="your_key_here"
```

3. Run the Streamlit app:

```bash
streamlit run app.py
```

## Data Model

`data/transformer_data.csv` contains synthetic but realistic feeder records with:

- `Feeder_ID`
- `Transformer_Capacity_kVA` (200-1000)
- `Current_Load_kVA` (60%-98% of capacity)
- `Temperature_C` (30-50)
- `Historical_Growth_Percent` (1-10)

## Why This Is Industry-Relevant

- Aligns with real feeder-loading and thermal-risk constraints
- Uses deterministic, auditable risk scoring suitable for utility governance
- Adds LLM-powered engineering narratives without replacing core logic
- Supports planning, maintenance prioritization, and operator communication
- Ready for hackathons, pilots, and extension into SCADA/AMI-backed workflows
