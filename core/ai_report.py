from __future__ import annotations

import os
from typing import Any

import google.generativeai as genai


def _build_prompt(feeder_metrics: dict[str, Any]) -> str:
    return f"""
You are a senior distribution utility planning and operations engineer.
Write a concise, formal technical report for this feeder.

Feeder Data:
- Feeder_ID: {feeder_metrics["Feeder_ID"]}
- Transformer_Capacity_kVA: {feeder_metrics["Transformer_Capacity_kVA"]}
- Current_Load_kVA: {feeder_metrics["Current_Load_kVA"]}
- Load_Ratio_Percent: {feeder_metrics["Load_Ratio_Percent"]}
- Temperature_C: {feeder_metrics["Temperature_C"]}
- Historical_Growth_Percent: {feeder_metrics["Historical_Growth_Percent"]}
- Risk_Score: {feeder_metrics["Risk_Score"]}
- Risk_Level: {feeder_metrics["Risk_Level"]}
- Engineering_Action: {feeder_metrics["Engineering_Action"]}

Required output sections:
1) Technical Situation Summary
2) Root Cause Reasoning
3) Recommended Utility Actions

Keep the tone formal, practical, and utility-engineering oriented.
Avoid marketing language.
""".strip()


def generate_ai_technical_report(
    feeder_metrics: dict[str, Any],
    model_name: str | None = None,
    api_key: str | None = None,
) -> str:
    resolved_api_key = api_key or os.getenv("GEMINI_API_KEY")
    if not resolved_api_key:
        raise RuntimeError("GEMINI_API_KEY is not set in the environment.")

    selected_model = model_name or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    genai.configure(api_key=resolved_api_key)
    model = genai.GenerativeModel(model_name=selected_model)
    prompt = _build_prompt(feeder_metrics)
    response = model.generate_content(prompt)
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()
