# app.py
import streamlit as st
import os
import json
from dotenv import load_dotenv

# Load local env (do NOT commit .env)
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

st.set_page_config(page_title="CareerPilot (Demo)", layout="centered")

st.title("CareerPilot — Placement Readiness Demo")
st.caption("Multi-agent demo: Profile Collector → Evaluator → Gap Detector → Roadmap")

# Sidebar: API Key check
st.sidebar.header("Settings")
if not GOOGLE_API_KEY:
    st.sidebar.error("No GOOGLE_API_KEY found. Put it in .env")
else:
    st.sidebar.success("API key loaded (hidden)")

# --- Input form ---
st.header("Student Profile Input")
with st.form(key="profile_form"):
    name = st.text_input("Full name")
    cgpa = st.text_input("CGPA (0-10) — leave blank if unknown")
    skills = st.text_area("Skills (comma separated)", "Python, DSA, Machine Learning")
    projects = st.text_area("Projects (one per line)", "Project 1\nProject 2")
    cp_experience = st.text_input("Competitive programming (rating / brief)")
    career_goal = st.text_input("Career goal (e.g., Product-based Software Engineer)")
    dsa_count = st.number_input("No. of DSA problems solved (estimate)", min_value=0, step=1, value=0)
    internships = st.number_input("Number of internships", min_value=0, step=1, value=0)
    submit = st.form_submit_button("Run Agents")

if submit:
    # Build input text (or dict) for Agent 1
    raw_text = f"""
    Name: {name}
    CGPA: {cgpa}
    Skills: {skills}
    Projects: {projects}
    CP: {cp_experience}
    Career goal: {career_goal}
    DSA solved: {int(dsa_count)}
    Internships: {int(internships)}
    """

    st.markdown("**Raw input sent to Agent 1:**")
    st.code(raw_text.strip())

    # --- Import your agent classes lazily to avoid import-time errors ---
    try:
        from first_agent import ProfileCollectorAgent, model as shared_model
        from second_agent import ReadinessEvaluatorAgent
        from third_agent import GapDetectorAgent
        from fourth_agent import RoadmapAgent
    except Exception as e:
        st.error(f"Error importing agent modules: {e}")
        st.stop()

    # --- Agent 1: collect profile ---
    try:
        pc_agent = ProfileCollectorAgent(shared_model)
        profile = pc_agent.collect(raw_text)   # adapt name if your method differs
        st.success("Agent 1 (Profile Collector) finished")
        st.json(profile)
    except Exception as e:
        st.error(f"Agent 1 failed: {e}")
        st.stop()

    # --- Agent 2: readiness eval ---
    try:
        eval_agent = ReadinessEvaluatorAgent()
        evaluation = eval_agent.evaluate(profile)
        st.success("Agent 2 (Readiness Evaluator) finished")
        st.json(evaluation)
    except Exception as e:
        st.error(f"Agent 2 failed: {e}")
        st.stop()

    # --- Agent 3: gap detection ---
    try:
        gap_agent = GapDetectorAgent()
        gaps = gap_agent.find_gap(profile=profile, evaluation=evaluation)
        st.success("Agent 3 (Gap Detector) finished")
        st.json(gaps)
    except Exception as e:
        st.error(f"Agent 3 failed: {e}")
        st.stop()

    # --- Agent 4: roadmap generation ---
    try:
        roadmap_agent = RoadmapAgent()
        roadmap = roadmap_agent.generate_roadmap(profile=profile, evaluation=evaluation, gaps=gaps)
        st.success("Agent 4 (Roadmap Generator) finished")
        st.json(roadmap)
    except Exception as e:
        st.error(f"Agent 4 failed: {e}")
        st.stop()

    # Show summary
    st.header("Summary")
    st.markdown(f"**Overall score:** {evaluation.get('overall_score')}")
    st.markdown("**Final recommendations (short):**")
    st.write(gaps.get("final_summary", roadmap.get("short_summary", "—")))
