# fourth_agent.py

import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


class RoadmapAgent:
    def __init__(self):
        pass

    def generate_roadmap(self, profile: dict, evaluation: dict, gaps: dict):
        """
        Creates a 7-day personalized roadmap based on student's career goal,
        their readiness evaluation, and identified gaps.
        """

        prompt = f"""
You are a Roadmap Generator Agent. Based on the student's profile, evaluation scores,
and gap analysis, create a personalized **7-day improvement roadmap**.

### Student Profile:
{json.dumps(profile, indent=2)}

### Evaluation Output:
{json.dumps(evaluation, indent=2)}

### Gaps Identified:
{json.dumps(gaps, indent=2)}

### INSTRUCTIONS:
Create a 7-day roadmap in **strict JSON format**, following this structure:

{{
  "career_goal": "string",
  "overall_readiness_level": "Highly Ready / Moderately Ready / Needs Improvement / Poor",
  "day_wise_plan": {{
    "Day 1": "task",
    "Day 2": "task",
    "Day 3": "task",
    "Day 4": "task",
    "Day 5": "task",
    "Day 6": "task",
    "Day 7": "task"
  }},
  "resources": {{
    "DSA": ["resource1", "resource2"],
    "Skills": ["resource1", "resource2"],
    "Projects": ["resource1", "resource2"]
  }},
  "final_advice": "short motivation and next steps"
}}

### RULES:
- The roadmap MUST depend on the student's **career goal**.
- Tailor the tasks to the student’s gaps:
  - If DSA score < 8 → include DSA improvement tasks.
  - If project score < 8 → include project-building tasks.
  - If skills score < 8 → include upskilling tasks.
- Keep each day’s task short, realistic, and actionable.
- Avoid extra commentary—return **ONLY the JSON**.

Now generate the roadmap.
"""

        response = model.generate_content(prompt)

        # Clean LLM output
        clean_output = response.text.strip()
        clean_output = clean_output.replace("```json", "").replace("```", "").strip()

        try:
            result = json.loads(clean_output)
        except json.JSONDecodeError:
            raise ValueError("LLM returned invalid JSON. Raw output:\n" + response.text)

        return result
