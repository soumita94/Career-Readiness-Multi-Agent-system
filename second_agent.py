# agent2_readiness.py

import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

class ReadinessEvaluatorAgent:

    def __init__(self):
        pass

    def evaluate(self, profile: dict):
        """
        profile is the JSON dict received from Agent 1.
        """

        prompt = f"""
You are an evaluation agent. Evaluate this student's readiness based on
their skills, projects, DSA experience, academics, and career goal.

Your scoring system:
- Skills score: 0-10
- Project score: 0-10
- DSA score: 0-10
- Academic score (based on CGPA): 0-10

Different career goals have different weight:
- AI Engineer: skills + projects more important
- Software Engineer / Product: DSA more important
- Startup Entrepreneur: skills + projects highest, academics low importance
- Higher Studies: academics highest weight

Input student profile (JSON):
{json.dumps(profile, indent=2)}

Output a JSON exactly in this format:

{{
  "scores": {{
    "skills": number,
    "projects": number,
    "dsa": number,
    "academics": number
  }},
  "overall_score": number,
  "summary": "short analysis text"
}}
"""

        response = model.generate_content(prompt)

        try:
            clean_output = response.text.strip()
            clean_output = clean_output.replace("```json", "").replace("```", "").strip()
            result = json.loads(clean_output)
        except:
            raise ValueError("LLM failed to return valid JSON. Raw output:\n" + response.text)

        return result
