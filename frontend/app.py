from __future__ import annotations

import httpx
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Enterprise Hospital Dashboard",
    page_icon="🏥",
    layout="wide",
)

API_BASE_URL = "http://localhost:8000"

HEADER_CSS = """
<style>
body {
    background: linear-gradient(135deg, #0f2a1a 0%, #1a3d2e 50%, #0a1d14 100%);
}
section.main {
    background: rgba(15, 42, 26, 0.98);
}
.css-1d391kg {
    color: #f0f8f0;
}
.dashboard-card {
    border: 1px solid rgba(40, 167, 69, 0.3);
    border-radius: 20px;
    padding: 24px;
    background: rgba(40, 167, 69, 0.08);
    backdrop-filter: blur(12px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(40, 167, 69, 0.2);
}
.metric-title {
    color: #28A745;
    font-size: 0.95rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.metric-value {
    color: #FFFFFF;
    font-size: 2.3rem;
    font-weight: 700;
}
.status-chip {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 8px 16px;
    border-radius: 25px;
    background: rgba(40, 167, 69, 0.2);
    color: #28A745;
    font-weight: 600;
    margin-bottom: 16px;
    box-shadow: 0 4px 12px rgba(40, 167, 69, 0.2);
}
.status-chip.rejected {
    background: rgba(220, 53, 69, 0.2);
    color: #DC3545;
    box-shadow: 0 4px 12px rgba(220, 53, 69, 0.3);
}
.hospital-icon {
    font-size: 2rem;
    margin-right: 12px;
}
</style>
"""

st.markdown(HEADER_CSS, unsafe_allow_html=True)

st.markdown(
    """
    <div style='display:flex; justify-content:space-between; align-items:center; gap:16px;'>
        <div style='display: flex; align-items: center;'>
            <span class='hospital-icon'>🏥⚕️</span>
            <div>
                <p style='margin:0; color:#28A745; letter-spacing:0.16em; text-transform:uppercase; font-size:0.85rem; font-weight: bold;'>Hospital Intelligence Platform</p>
                <h1 style='margin:4px 0 0; color:#FFFFFF; font-size: 2.4rem;'><span style='color: #28A745;'>💊 </span>Enterprise Clinical Dashboard</h1>
                <p style='margin:8px 0 0; color:#D4EDDA; max-width:720px; font-size: 1.05rem;'>AI-powered clinical decision support: personalized medication recommendations, interaction screening, risk assessment &amp; alternatives.</p>
            </div>
        </div>
        <div style='text-align:right;'>
            <span class='status-chip'>🟢 API Connected</span>
            <p style='margin:4px 0 0; color:#28A745; font-size:1rem; font-weight:500;'>{API_BASE_URL}</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


def fetch_diseases() -> list[str]:
    try:
        response = httpx.get(f"{API_BASE_URL}/diseases", timeout=8.0)
        response.raise_for_status()
        return response.json().get("diseases", [])
    except Exception:
        return []


def request_recommendation(payload: dict) -> dict:
    try:
        response = httpx.post(
            f"{API_BASE_URL}/recommend",
            json=payload,
            timeout=16.0,
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        return {
            "error": "API request failed.",
            "detail": exc.response.json() if exc.response is not None else str(exc),
        }
    except Exception as exc:
        return {"error": "Unable to connect to backend.", "detail": str(exc)}


def build_request_payload() -> dict:
    st.sidebar.markdown("## Patient profile")
    age = st.sidebar.number_input("Patient age", min_value=0, max_value=120, value=45)
    disease = st.sidebar.selectbox("Primary condition", fetch_diseases() or ["hypertension", "diabetes", "asthma"])
    allergies = st.sidebar.text_area(
        "Allergies (comma-separated)", value="penicillin, aspirin",
        help="Enter common allergens separated by commas.",
    )
    history = st.sidebar.text_area(
        "Clinical history (comma-separated)", value="hypertension, high cholesterol",
        help="Enter relevant conditions or procedures separated by commas.",
    )
    medications = st.sidebar.text_area(
        "Current medications (comma-separated)", value="metformin, lisinopril",
        help="Enter active medications separated by commas.",
    )
    show_api = st.sidebar.checkbox("Show raw API payload", value=False)

    payload = {
        "age": age,
        "disease": disease,
        "allergies": [item.strip() for item in allergies.split(",") if item.strip()],
        "history": [item.strip() for item in history.split(",") if item.strip()],
        "current_medications": [item.strip() for item in medications.split(",") if item.strip()],
    }

    if show_api:
        st.sidebar.code(payload)

    return payload


payload = build_request_payload()

with st.container():
    if st.button("Run Clinical Recommendation", type="primary"):
        result = request_recommendation(payload)

        if result.get("error"):
            st.error("Could not fetch recommendations. Check the backend URL and API status.")
            st.json(result.get("detail", result))
        else:
            summary = result.get("graph_summary", {})
            accepted = result.get("accepted", [])
            rejected = result.get("rejected", [])

            summary_cols = st.columns(4)
            summary_cols[0].metric("🏥 Diseases", len(fetch_diseases()))
            summary_cols[1].metric("✅ Accepted", len(accepted))
            summary_cols[2].metric("❌ Rejected", len(rejected))
            summary_cols[3].metric("📈 Graph Nodes", summary.get("nodes", 0))

            # Risk overview chart
            fig = px.pie(
                values=[len(accepted), len(rejected)],
                names=["Accepted", "Rejected"],
                color_discrete_map={"Accepted": "#28A745", "Rejected": "#DC3545"},
                title="Recommendation Risk Distribution"
            )
            fig.update_traces(textposition="inside", textinfo="percent+label")
            fig.update_layout(showlegend=False, font_color="white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

            st.markdown("<div class='dashboard-card'>", unsafe_allow_html=True)
            st.markdown("<div class='metric-title'>Clinical recommendation overview</div>", unsafe_allow_html=True)
            st.markdown(
                "<p style='color:#D4EDDA; margin:0 0 20px; font-size: 1.05rem; line-height:1.5;'><span style='color:#28A745; font-weight:bold; font-size:1.1rem;'>⚕️ Clinical Insights</span><br>The dashboard below details medication decisions, risk scores, reasoning, and evidence-based alternatives from the AI clinical engine.</p>",
                unsafe_allow_html=True,
            )

            accepted_col, rejected_col = st.columns(2)
            with accepted_col:
                st.subheader("Accepted Medications")
                if accepted:
                    for item in accepted:
                        st.markdown(f"### {item['drug']}  ")
                        st.markdown(f"**Risk score:** {item['risk_score']}  ")
                        st.markdown("**Reasoning:**")
                        for reason in item["reasons"]:
                            st.markdown(f"- {reason}")
                        if item["alternatives_considered"]:
                            st.markdown("**Alternatives considered:**")
                            for alt in item["alternatives_considered"]:
                                st.markdown(f"- {alt}")
                        st.markdown("---")
                else:
                    st.info("No accepted medications returned.")

            with rejected_col:
                st.subheader("Rejected Medications")
                if rejected:
                    for item in rejected:
                        st.markdown(f"### {item['drug']}  ")
                        st.markdown("**Reasons:**")
                        for reason in item["reasons"]:
                            st.markdown(f"- {reason}")
                        if item["alternatives"]:
                            st.markdown("**Alternatives:**")
                            for alt in item["alternatives"]:
                                st.markdown(f"- {alt}")
                        st.markdown("---")
                else:
                    st.info("No rejected medications returned.")

            st.markdown("</div>", unsafe_allow_html=True)

            with st.expander("View raw recommendation response", expanded=False):
                st.json(result)

    else:
        st.warning("Submit the patient profile to generate the hospital dashboard recommendation.")
        st.info("Use the sidebar to customize age, condition, allergies, history, and current medications.")
