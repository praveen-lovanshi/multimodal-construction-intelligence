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
    st.markdown("<div class='eyebrow'>MULTIMODAL CONSTRUCTION INTELLIGENCE <span>V2.0 · STUDENT EDITION</span></div>", unsafe_allow_html=True)
    st.title("Construction Decision Support Dashboard")
    st.caption("Multimodal AI for site safety, structural health, planning, valuation, and daily coordination")
    st.warning("Decision-support only: verify safety, structural, cost, and code decisions with qualified professionals.")


def metric_card(label: str, value: str, detail: str, tone: str = "orange") -> None:
    st.markdown(
        f"<div class='metric-card {tone}'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div><div class='metric-detail'>{detail}</div></div>",
        unsafe_allow_html=True,
    )


def module_card(icon: str, title: str, description: str, tag: str, tone: str = "orange") -> None:
    st.markdown(
        f"<div class='module-card'><div class='module-icon {tone}'>{icon}</div><div class='module-tag {tone}'>{tag}</div><h3>{title}</h3><p>{description}</p><div class='launch {tone}'>Open workspace →</div></div>",
        unsafe_allow_html=True,
    )


def overview_tab() -> None:
    st.markdown("<div class='hero-row'><div><h2>Project overview</h2><p>One workspace for construction intelligence and field decisions.</p></div><div class='api-pill'>● DEMO MODE</div></div>", unsafe_allow_html=True)
    st.button("Generate full site audit", type="primary", use_container_width=False)
    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("SITE SAFETY SCORE", "82/100", "Needs attention · PPE audit", "orange")
    with c2: metric_card("ACTIVE DEFECT SEVERITY", "Minor", "Hairline · Review advised", "red")
    with c3: metric_card("PROJECT BUDGET", "₹25.2 L", "Indicative · 25% complete", "green")
    with c4: metric_card("SCHEDULE TIMELINE", "12 weeks", "Milestone plan · On track", "blue")
    st.markdown("<div class='alert-card'><b>⚠ HIGH PRIORITY SITE CHECK</b><br><span>Review PPE compliance, access routes, and weather conditions before beginning elevated or lifting work.</span></div>", unsafe_allow_html=True)
    st.subheader("Intelligence modules")
    c1, c2, c3 = st.columns(3)
    with c1: module_card("🛡", "Site safety monitoring", "PPE checks, hazard severity, and corrective actions from construction photos.", "82% DEMO SCORE", "orange")
    with c2: module_card("⌁", "Crack diagnostics", "Defect classification, estimated width, causes, urgency, and repair guidance.", "MINOR DEFECT", "red")
    with c3: module_card("₹", "Valuation studio", "Budget, capex, material quantities, and indicative Indian market valuation.", "INR READY", "green")
    c1, c2, c3 = st.columns(3)
    with c1: module_card("▦", "WBS & planning", "Construction phases, quantities, milestones, and completion progress.", "12-WEEK PLAN", "blue")
    with c2: module_card("☁", "Weather advisory", "GO / NO-GO guidance for rain, wind, heat, and weather-sensitive activities.", "RISK AWARE", "orange")
    with c3: module_card("▣", "Knowledge assistant", "Ask concise construction questions and receive practical site guidance.", "READY", "green")


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
    st.subheader("Daily Site Assistant")
    st.caption("Ask practical construction questions and keep today’s coordination notes in one place.")
    weather = st.selectbox("Current site condition", ["Normal", "High Wind", "Heavy Rain", "Extreme Heat"])
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


def weather_tab() -> None:
    st.subheader("Weather Advisory")
    st.caption("Make a clear GO / NO-GO decision before weather-sensitive construction work begins.")
    c1, c2 = st.columns([1, 1.3])
    with c1:
        activity = st.text_input("Planned activity", value="Slab concreting", key="weather_activity")
        weather = st.selectbox("Current / forecast weather", ["Normal", "High Wind", "Heavy Rain", "Extreme Heat"], key="weather_condition")
        check = st.button("Check feasibility", type="primary", use_container_width=True)
    advisories = {
        "Normal": ("GO", "Proceed with normal controls and a toolbox talk.", ["Verify PPE and access routes", "Confirm equipment inspection", "Maintain housekeeping"]),
        "High Wind": ("NO-GO FOR EXPOSED LIFTING", "Suspend crane and elevated work when wind exceeds equipment limits.", ["Secure loose materials", "Check tower crane wind limits", "Review work-at-height controls"]),
        "Heavy Rain": ("NO-GO FOR ELECTRICAL EXPOSURE", "Protect electrical systems and stop work in flooded or slippery areas.", ["Isolate exposed electrical equipment", "Protect fresh concrete and materials", "Inspect access routes before restart"]),
        "Extreme Heat": ("GO WITH CONTROLS", "Use hydration, shaded rest, heat monitoring, and cooler work periods.", ["Schedule breaks and hydration", "Monitor heat stress symptoms", "Shift heavy work to cooler hours"]),
    }
    decision, advice, risks = advisories[weather]
    with c2:
        items = "".join(f"<div class='advisory-item'>✓ {risk}</div>" for risk in risks)
        tone = "good" if weather == "Normal" else "caution"
        st.markdown(f"<div class='advisory-card {tone}'><div class='advisory-kicker'>WEATHER DECISION</div><h2>{decision}</h2><p>{advice}</p><div class='advisory-label'>REQUIRED PRECAUTIONS</div>{items}</div>", unsafe_allow_html=True)
    if check:
        st.success(f"Advisory generated for **{activity}** under **{weather}** conditions.")


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="🏗️", layout="wide")
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
    :root { --bg:#070b14; --panel:#111a2d; --panel2:#172238; --text:#edf2fb; --muted:#8d9ab0; --orange:#ff9d00; --red:#ff4264; --green:#00c894; --blue:#25b9e8; }
    .stApp { background: radial-gradient(circle at 80% 0%, #18243a 0, var(--bg) 38%); color:var(--text); }
    .block-container { max-width: 1450px; padding: 2rem 3rem 4rem; }
    html, body, [class*='css'] { font-family:'DM Sans', sans-serif; }
    h1,h2,h3 { font-family:'Space Grotesk', sans-serif !important; color:var(--text) !important; }
    h1 { font-size:2.1rem !important; margin-bottom:.2rem !important; }
    h2 { font-size:1.35rem !important; }
    h3 { font-size:1rem !important; }
    p, .stCaption { color:var(--muted) !important; }
    [data-testid='stSidebar'] { background:#090e18; border-right:1px solid #202b40; }
    [data-testid='stSidebar'] h1 { color:var(--orange) !important; }
    [data-testid='stSidebar'] .stRadio label { color:#c5cfdf !important; padding:.35rem 0; }
    [data-testid='stSidebar'] .stRadio label:hover { color:var(--orange) !important; }
    .eyebrow { color:var(--orange); font-size:.72rem; letter-spacing:.14em; font-weight:700; margin-bottom:1rem; }
    .eyebrow span { color:var(--muted); margin-left:1rem; letter-spacing:.05em; }
    .hero-row { display:flex; justify-content:space-between; align-items:center; margin:1rem 0; }
    .hero-row h2 { margin-bottom:0; }
    .hero-row p { margin-top:.25rem; }
    .api-pill { border:1px solid #006f5a; color:var(--green); background:#052b28; border-radius:999px; padding:.55rem .9rem; font-size:.75rem; font-weight:700; }
    .metric-card, .module-card, .alert-card { background:linear-gradient(145deg,var(--panel),#0e1729); border:1px solid #25324b; border-radius:12px; box-shadow:0 8px 25px #0002; }
    .metric-card { min-height:120px; padding:1rem; border-left:3px solid var(--orange); margin-bottom:1rem; }
    .metric-card.red { border-left-color:var(--red); } .metric-card.green { border-left-color:var(--green); } .metric-card.blue { border-left-color:var(--blue); }
    .metric-label { color:var(--muted); font-size:.7rem; font-weight:700; letter-spacing:.08em; }
    .metric-value { font-family:'Space Grotesk'; font-size:1.75rem; font-weight:700; margin:.55rem 0 .25rem; }
    .metric-detail { color:var(--muted); font-size:.75rem; }
    .alert-card { border-color:#7d243b; background:#281321; padding:1rem 1.2rem; margin:1rem 0 2rem; color:#ff5572; }
    .alert-card span { color:#c7a9b2; font-size:.8rem; }
    .module-card { min-height:170px; padding:1.15rem; margin-bottom:1rem; position:relative; }
    .module-card h3 { margin:.7rem 0 .35rem; } .module-card p { font-size:.82rem; min-height:42px; }
    .module-icon { width:32px; height:32px; display:flex; align-items:center; justify-content:center; border-radius:8px; background:#29334b; font-size:1.1rem; }
    .advisory-card { background:linear-gradient(145deg,var(--panel),#0e1729); border:1px solid #25324b; border-left:3px solid var(--orange); border-radius:12px; padding:1.4rem; min-height:220px; }
    .advisory-card.good { border-left-color:var(--green); } .advisory-card.caution { border-left-color:var(--orange); }
    .advisory-kicker, .advisory-label { color:var(--muted); font-size:.7rem; font-weight:700; letter-spacing:.08em; }
    .advisory-card h2 { color:var(--orange) !important; margin:.6rem 0; } .advisory-card.good h2 { color:var(--green) !important; }
    .advisory-item { background:#0b1323; border-radius:6px; padding:.5rem; margin-top:.45rem; color:#c9d2e2; font-size:.8rem; }
    .module-tag { position:absolute; top:1rem; right:1rem; font-size:.62rem; padding:.28rem .45rem; border-radius:5px; background:#4a3818; color:var(--orange); }
    .module-tag.red { background:#421b2b; color:#ff5472; } .module-tag.green { background:#083a35; color:var(--green); } .module-tag.blue { background:#08364b; color:var(--blue); }
    .launch { color:var(--orange); font-size:.76rem; font-weight:700; } .launch.green { color:var(--green); } .launch.blue { color:var(--blue); } .launch.red { color:var(--red); }
    .stButton > button { background:linear-gradient(135deg,#ffb000,#f07e00); color:#111; border:0; font-weight:700; border-radius:8px; }
    .stButton > button:hover { background:#ffc04a; color:#111; }
    [data-testid='stMetric'] { background:var(--panel); border:1px solid #25324b; border-radius:10px; }
    [data-baseweb='tab-list'] { gap: .35rem; } [data-baseweb='tab'] { color:var(--muted); } [aria-selected='true'] { color:var(--orange) !important; }
    [data-testid='stFileUploaderDropzone'], [data-testid='stChatInput'], [data-testid='stChatInput'] > div { background:var(--panel) !important; border:1px dashed #3b4964 !important; }
    [data-testid='stChatInput'] textarea, input, textarea, [data-baseweb='select'] > div { background:#111a2d !important; color:#edf2fb !important; border-color:#3b4964 !important; }
    [data-testid='stHeader'], [data-testid='stToolbar'], header { background:transparent !important; }
    </style>
    """, unsafe_allow_html=True)
    with st.sidebar:
        st.markdown("# 🏗️\n**CONSTRUCT**<span style='color:#ff9d00'>AI</span>", unsafe_allow_html=True)
        st.caption("Full-stack construction decision support")
        st.divider()
        st.text_input("Gemini API key", type="password", key="gemini_api_key", help="Optional. Leave blank for demonstration mode.")
        st.caption("A configured Streamlit secret or GEMINI_API_KEY environment variable takes priority. Keys are not stored by this app.")
        st.divider()
        st.markdown("**SYSTEM STATUS**")
        st.success("● Demo system online")
        st.caption("v1.0 · Student certification build")
    show_header()
    page = st.radio("Navigation", ["Overview", "Site Safety (PPE)", "Crack Analysis", "Valuation Studio", "WBS & Planning", "Daily Site Log", "Weather Advisory"], horizontal=True, label_visibility="collapsed")
    if page == "Overview": overview_tab()
    elif page == "Site Safety (PPE)": safety_tab()
    elif page == "Crack Analysis": crack_tab()
    elif page == "Valuation Studio": planning_tab()
    elif page == "WBS & Planning": planning_tab()
    elif page == "Daily Site Log": assistant_tab()
    else: weather_tab()


if __name__ == "__main__":
    main()
