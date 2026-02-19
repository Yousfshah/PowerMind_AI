from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class RiskThresholds:
    temperature_start_c: float = 40.0
    growth_start_percent: float = 5.0
    max_score: float = 120.0


def _compute_risk_score(
    capacity_kva: float,
    load_kva: float,
    temperature_c: float,
    growth_percent: float,
    thresholds: RiskThresholds,
) -> float:
    load_ratio_percent = (load_kva / capacity_kva) * 100.0

    temperature_penalty = max(0.0, (temperature_c - thresholds.temperature_start_c) * 1.8)
    growth_penalty = max(0.0, (growth_percent - thresholds.growth_start_percent) * 2.2)

    raw_score = load_ratio_percent + temperature_penalty + growth_penalty
    return float(np.clip(raw_score, 0.0, thresholds.max_score))


def _classify_risk(score: float) -> str:
    if score <= 80:
        return "Low"
    if score <= 95:
        return "Medium"
    return "High"


def _engineering_action(
    risk_level: str,
    load_ratio_percent: float,
    temperature_c: float,
    growth_percent: float,
) -> str:
    if risk_level == "High":
        if load_ratio_percent >= 95:
            return "Immediate load transfer and capacity augmentation planning required."
        if temperature_c > 45:
            return "Urgent thermal inspection, oil diagnostics, and cooling intervention required."
        return "Priority feeder reinforcement and contingency switching plan required."
    if risk_level == "Medium":
        if growth_percent > 7:
            return "Initiate 6-12 month expansion plan with targeted network balancing."
        return "Increase monitoring frequency and schedule preventive maintenance in current cycle."
    return "Continue standard monitoring; maintain preventive maintenance and quarterly review."


def score_feeder_risk(df: pd.DataFrame, thresholds: RiskThresholds | None = None) -> pd.DataFrame:
    required_cols = {
        "Feeder_ID",
        "Transformer_Capacity_kVA",
        "Current_Load_kVA",
        "Temperature_C",
        "Historical_Growth_Percent",
    }
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    thresholds = thresholds or RiskThresholds()
    result = df.copy()
    result["Load_Ratio_Percent"] = (
        result["Current_Load_kVA"] / result["Transformer_Capacity_kVA"] * 100.0
    ).round(2)

    result["Risk_Score"] = result.apply(
        lambda row: _compute_risk_score(
            capacity_kva=float(row["Transformer_Capacity_kVA"]),
            load_kva=float(row["Current_Load_kVA"]),
            temperature_c=float(row["Temperature_C"]),
            growth_percent=float(row["Historical_Growth_Percent"]),
            thresholds=thresholds,
        ),
        axis=1,
    ).round(2)
    result["Risk_Level"] = result["Risk_Score"].apply(_classify_risk)
    result["Engineering_Action"] = result.apply(
        lambda row: _engineering_action(
            risk_level=row["Risk_Level"],
            load_ratio_percent=float(row["Load_Ratio_Percent"]),
            temperature_c=float(row["Temperature_C"]),
            growth_percent=float(row["Historical_Growth_Percent"]),
        ),
        axis=1,
    )
    return result
