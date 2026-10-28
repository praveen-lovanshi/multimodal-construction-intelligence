"""Multimodal Construction Intelligence Platform.

Streamlit capstone application with optional Gemini multimodal analysis.
The app remains fully usable in demonstration mode when no API key is set.
"""

from __future__ import annotations

import json
import os
from typing import Any

import streamlit as st

APP_TITLE = "Multimodal Construction Intelligence Platform"
SEVERITIES = ["Low", "Medium", "High", "Critical"]


def safe_json(text: str) -> dict[str, Any] | None:
    """Extract a JSON object from a model response."""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                return None
    return None


def ask_gemini(feature: str, prompt: str, uploaded_file: Any = None) -> dict[str, Any] | None:
    """Call Gemini if configured; return None so callers can use demo data otherwise."""
    try:
        secret_key = str(st.secrets.get("GEMINI_API_KEY", "")).strip()
    except Exception:
        secret_key = ""
    api_key = (secret_key or os.getenv("GEMINI_API_KEY", "") or st.session_state.get("gemini_api_key", "")).strip()
    if not api_key:
        return None
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            os.getenv("GEMINI_MODEL", "gemini-1.5-flash"),
            system_instruction=(
                "You are a construction engineering decision-support assistant. "
                "Return JSON only, with no markdown. Be cautious: outputs are indicative "
                "and never replace a licensed engineer, safety officer, or local code review."
            ),
        )
        parts: list[Any] = [f"Feature: {feature}\n{prompt}"]
        if uploaded_file is not None:
            parts.append({"mime_type": uploaded_file.type, "data": uploaded_file.getvalue()})
        response = model.generate_content(parts)
        return safe_json(response.text or "")
    except Exception as exc:  # graceful fallback is intentional for cloud demos
        st.warning(f"AI service unavailable; showing demonstration output. ({exc})")
        return None


def download_json(data: dict[str, Any], filename: str) -> None:
    st.download_button(
        "Download JSON report",
        data=json.dumps(data, indent=2, ensure_ascii=False),
        file_name=filename,
        mime="application/json",
        use_container_width=True,
    )


def demo_safety() -> dict[str, Any]:
    return {
        "safety_score": 82,
        "overall_status": "Needs attention",
        "ppe_detection": {
            "helmets": {"status": "Detected", "coverage": "Most workers"},
            "high_visibility_vests": {"status": "Partial", "coverage": "Some workers"},
            "steel_toe_boots": {"status": "Not verifiable", "coverage": "Image limitation"},
            "safety_harnesses": {"status": "Not required / not visible", "coverage": "Elevated work not confirmed"},
        },
        "hazards": [
            {"hazard": "Unsegregated debris near walkway", "severity": "Medium", "remedy": "Clear access route and establish housekeeping checks."},
            {"hazard": "High-visibility vest compliance is inconsistent", "severity": "Medium", "remedy": "Issue compliant vests before entry and enforce gate checks."},
        ],
        "limitations": ["Demonstration output; confirm conditions in person."],
    }


def demo_crack() -> dict[str, Any]:
    return {
        "defect_type": "Hairline",
        "estimated_crack_width_mm": 0.3,
        "severity": "Minor",
        "root_causes": ["Drying shrinkage", "Thermal movement"],
        "potential_risks": ["Water ingress if crack propagates", "Cosmetic deterioration"],
        "recommended_repairs": ["Map and monitor crack", "Seal with suitable flexible sealant after engineer review"],
        "urgency": "Routine inspection",
        "limitations": ["Image-based estimate only; use a crack gauge and professional inspection."],
    }


def show_header() -> None:
    st.title(APP_TITLE)
    st.caption("AI-assisted construction planning, safety, diagnostics, and site coordination")
    st.info("Decision-support only: verify safety, structural, cost, and code decisions with qualified professionals.")


def safety_tab() -> None:
    st.subheader("Site Safety & PPE Audit")
    uploaded = st.file_uploader("Upload a construction site photo", type=["jpg", "jpeg", "png"], key="safety_image")
    description = st.text_area("Optional site description", placeholder="Example: slab work at 3 m height; rain started 20 minutes ago.", key="safety_desc")
    if uploaded:
        st.image(uploaded, caption="Uploaded site photo", use_container_width=True)
    if st.button("Run safety audit", type="primary", use_container_width=True):
        prompt = f"Analyze PPE, worker positioning, fall risks, access routes, debris, lighting, and environmental hazards. Context: {description}. Return keys safety_score, overall_status, ppe_detection, hazards, limitations. Use severity values Low, Medium, High, or Critical."
        result = ask_gemini("safety audit", prompt, uploaded) or demo_safety()
        st.session_state["safety_result"] = result
    result = st.session_state.get("safety_result")
    if result:
        c1, c2, c3 = st.columns(3)
        c1.metric("Safety score", f"{result.get('safety_score', 0)}/100")
        c2.metric("Status", result.get("overall_status", "Unknown"))
        c3.metric("Hazards", len(result.get("hazards", [])))
        st.json(result.get("ppe_detection", {}))
        for hazard in result.get("hazards", []):
            severity = hazard.get("severity", "Medium")
            color = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Critical": "🔴"}.get(severity, "⚪")
            st.warning(f"{color} **{severity}: {hazard.get('hazard', 'Unspecified hazard')}** — {hazard.get('remedy', 'Review with the safety officer.')}")
        download_json(result, "safety_audit.json")


def crack_tab() -> None:
    st.subheader("Crack Diagnostics & Structural Integrity")
    uploaded = st.file_uploader("Upload a concrete or wall image", type=["jpg", "jpeg", "png"], key="crack_image")
    description = st.text_area("Optional inspection context", placeholder="Example: crack appeared after heavy rain; located above a door opening.", key="crack_desc")
    if uploaded:
        st.image(uploaded, caption="Uploaded crack image", use_container_width=True)
    if st.button("Assess crack", type="primary", use_container_width=True):
        prompt = f"Classify the visible defect as Hairline, Settlement, Structural Shear, Thermal Expansion, or Spalling. Estimate crack width in mm, causes, risks, repairs, and urgency. Context: {description}. Return JSON keys defect_type, estimated_crack_width_mm, severity, root_causes, potential_risks, recommended_repairs, urgency, limitations."
        result = ask_gemini("crack diagnostics", prompt, uploaded) or demo_crack()
        st.session_state["crack_result"] = result
    result = st.session_state.get("crack_result")
    if result:
        c1, c2, c3 = st.columns(3)
        c1.metric("Defect type", result.get("defect_type", "Unknown"))
        c2.metric("Estimated width", f"{result.get('estimated_crack_width_mm', 0)} mm")
        c3.metric("Urgency", result.get("urgency", "Review"))
        st.write("**Potential causes**")
        st.write(" • ".join(result.get("root_causes", [])))
        st.write("**Recommended engineering actions**")
        for item in result.get("recommended_repairs", []):
            st.write(f"- {item}")
        download_json(result, "crack_diagnostics.json")


def planning_tab() -> None:
    st.subheader("Planning & Real Estate Valuation")
    c1, c2 = st.columns(2)
    with c1:
        structure = st.selectbox("Structure type", ["Residential RCC", "Commercial RCC", "Industrial shed", "Renovation"])
        area = st.number_input("Built-up area (sq ft)", min_value=100, value=1200, step=50)
        location = st.selectbox("Location tier", ["Tier 1", "Tier 2", "Tier 3"])
    with c2:
        completion = st.slider("Completion percentage", 0, 100, 25)
        age = st.number_input("Property age (years)", min_value=0, value=0, step=1)
        amenities = st.multiselect("Amenities", ["Parking", "Lift", "Power backup", "Security", "Solar"])
    if st.button("Generate plan & valuation", type="primary", use_container_width=True):
        rates = {"Tier 1": 2800, "Tier 2": 2100, "Tier 3": 1600}
        build_rate = {"Residential RCC": 2100, "Commercial RCC": 2600, "Industrial shed": 1500, "Renovation": 1200}[structure]
        budget = area * build_rate
        market = area * rates[location] * (1 + min(len(amenities) * 0.03, 0.15)) * max(0.75, 1 - age * 0.01)
        result = {
            "inputs": {"structure_type": structure, "built_up_sqft": area, "location_tier": location, "completion_percentage": completion, "property_age_years": age, "amenities": amenities},
            "total_project_budget_inr": round(budget),
            "capital_expenditure_incurred_inr": round(budget * completion / 100),
            "current_market_asset_valuation_inr": round(market),
            "price_per_sqft_inr": round(market / area),
            "estimated_materials": {"cement_bags": round(area * 0.42), "steel_kg": round(area * 4.2), "sand_cubic_ft": round(area * 0.9), "aggregate_cubic_ft": round(area * 1.7)},
            "milestones": [{"phase": "Foundation", "status": "Complete" if completion >= 25 else "Pending"}, {"phase": "Structure", "status": "Complete" if completion >= 60 else "In progress"}, {"phase": "Finishes", "status": "Complete" if completion >= 90 else "Pending"}],
            "disclaimer": "Indicative estimate; validate local rates, quantities, taxes, approvals, and engineering design.",
        }
        st.session_state["planning_result"] = result
    result = st.session_state.get("planning_result")
    if result:
        c1, c2, c3 = st.columns(3)
        c1.metric("Budget", f"₹{result['total_project_budget_inr'] / 100000:.1f} L")
        c2.metric("Incurred", f"₹{result['capital_expenditure_incurred_inr'] / 100000:.1f} L")
        c3.metric("Market valuation", f"₹{result['current_market_asset_valuation_inr'] / 100000:.1f} L")
        st.progress(result["inputs"]["completion_percentage"] / 100)
        st.write("**Material estimates**")
        st.json(result["estimated_materials"])
        st.caption(result["disclaimer"])
        download_json(result, "planning_valuation.json")


def assistant_tab() -> None:
    st.subheader("Daily Site Assistant & Weather Advisory")
    weather = st.selectbox("Current weather", ["Normal", "High Wind", "Heavy Rain", "Extreme Heat"])
    activity = st.text_input("Planned activity", placeholder="Example: concrete pour, crane lift, exterior painting")
    advisories = {
        "Normal": ("GO", "Continue with normal controls; verify daily toolbox talk and housekeeping."),
        "High Wind": ("NO-GO for exposed lifting", "Suspend crane and elevated work when wind exceeds equipment limits; secure loose materials."),
        "Heavy Rain": ("NO-GO for electrical exposure", "Protect electrical systems, stop work in flooded areas, and review concrete curing and access."),
        "Extreme Heat": ("GO with controls", "Use hydration, shaded rest, heat monitoring, and shift high-exertion work to cooler hours."),
    }
    decision, advice = advisories[weather]
    st.warning(f"**{decision}** — {advice}")
    if activity:
        st.caption(f"Advisory context: {activity}")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    query = st.chat_input("Ask a construction engineering question")
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        prompt = f"Answer concisely for a construction site engineer. Weather: {weather}. Planned activity: {activity}. Question: {query}. Provide practical steps, risks, and when to escalate to a qualified professional."
        ai = ask_gemini("construction assistant", prompt)
        answer = ai.get("answer", "Please verify this situation with the site engineer and safety officer.") if ai else "For a safe response, confirm site conditions, applicable local codes, equipment limits, and the responsible engineer's approval before proceeding."
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.rerun()


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="🏗️", layout="wide")
    st.markdown("""<style>.stApp {background: #f7f8fa;} .block-container {max-width: 1200px; padding-top: 2rem;} [data-testid='stMetric'] {background: white; padding: 1rem; border-radius: .75rem; box-shadow: 0 1px 5px #0001;}</style>""", unsafe_allow_html=True)
    with st.sidebar:
        st.header("🏗️ Platform controls")
        st.text_input("Gemini API key", type="password", key="gemini_api_key", help="Optional. Leave blank for demonstration mode.")
        st.caption("A configured Streamlit secret or GEMINI_API_KEY environment variable takes priority. Keys are not stored by this app.")
        st.divider()
        st.markdown("**Architecture**\n\nStreamlit UI → feature modules → optional Gemini multimodal layer → validated JSON → downloadable reports")
        st.markdown("**Deployment**\n\nWorks locally and on Streamlit Community Cloud with no database.")
    show_header()
    tabs = st.tabs(["Safety & PPE", "Crack Diagnostics", "Planning & Valuation", "Daily Assistant"])
    with tabs[0]: safety_tab()
    with tabs[1]: crack_tab()
    with tabs[2]: planning_tab()
    with tabs[3]: assistant_tab()


if __name__ == "__main__":
    main()
