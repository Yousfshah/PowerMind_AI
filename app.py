from __future__ import annotations

import pandas as pd
import streamlit as st

from core.ai_report import generate_ai_technical_report
from core.risk_engine import score_feeder_risk


def _risk_color(level: str) -> str:
    if level == "High":
        return "background-color: #f8d7da; color: #842029; font-weight: 600;"
    if level == "Medium":
        return "background-color: #fff3cd; color: #664d03; font-weight: 600;"
    return "background-color: #d1e7dd; color: #0f5132; font-weight: 600;"


def _render_risk_table(scored_df: pd.DataFrame) -> None:
    display_cols = [
        "Feeder_ID",
        "Transformer_Capacity_kVA",
        "Current_Load_kVA",
        "Load_Ratio_Percent",
        "Temperature_C",
        "Historical_Growth_Percent",
        "Risk_Score",
        "Risk_Level",
        "Engineering_Action",
    ]
    styled = scored_df[display_cols].style.map(_risk_color, subset=["Risk_Level"])
    st.dataframe(styled, use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="PowerMind AI", layout="wide")
    st.title("PowerMind AI - Distribution Network Risk & Loss Intelligence System")
    st.caption("Deterministic feeder risk analytics with Gemini-powered technical reporting")

    uploaded_file = st.file_uploader(
        "Upload feeder CSV",
        type=["csv"],
        help="Upload distribution feeder data to start risk analysis.",
    )

    st.sidebar.header("AI Configuration")
    model_name = st.sidebar.text_input(
        "Gemini model",
        value="gemini-2.5-flash",
        help="Example: gemini-2.5-flash",
    )
    manual_api_key = st.sidebar.text_input(
        "Gemini API key",
        type="password",
        help="Required. Paste your Gemini API key here.",
    )
    resolved_api_key = manual_api_key.strip()

    if uploaded_file is not None:
        feeder_df = pd.read_csv(uploaded_file)
    else:
        st.info("Upload a CSV file to run feeder risk analysis.")
        st.stop()

    try:
        scored_df = score_feeder_risk(feeder_df)
    except Exception as exc:
        st.error(f"Input validation failed: {exc}")
        return

    st.subheader("Feeder Risk Intelligence Table")
    _render_risk_table(scored_df)

    st.subheader("Individual Feeder Analysis")
    feeder_id = st.selectbox("Select Feeder", scored_df["Feeder_ID"].tolist())
    selected_row = scored_df.loc[scored_df["Feeder_ID"] == feeder_id].iloc[0].to_dict()

    col1, col2, col3 = st.columns(3)
    col1.metric("Risk Score", f'{selected_row["Risk_Score"]:.2f}')
    col2.metric("Risk Level", selected_row["Risk_Level"])
    col3.metric("Load Ratio (%)", f'{selected_row["Load_Ratio_Percent"]:.2f}')

    st.markdown("**Engineering Action**")
    st.write(selected_row["Engineering_Action"])

    if st.button("Generate AI Technical Report", type="primary"):
        if not resolved_api_key:
            st.error("Please enter Gemini API key in the sidebar.")
            st.stop()
        with st.spinner("Generating technical report from Gemini..."):
            try:
                report = generate_ai_technical_report(
                    selected_row,
                    model_name=model_name.strip() or None,
                    api_key=resolved_api_key,
                )
            except Exception as exc:
                st.error(f"AI report generation failed: {exc}")
            else:
                st.markdown("### Gemini Technical Report")
                st.write(report)


if __name__ == "__main__":
    main()
