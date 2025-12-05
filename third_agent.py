import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

class GapDetectorAgent:

    def __init__(self):
        pass

    def find_gap(self, profile: dict, evaluation: dict):
        """
        profile = JSON from Agent 1
        evaluation = JSON from Agent 2
        """

        prompt = f"""
You are a Gap Analysis Agent. 
Your job is to determine how far the student is from meeting the expectations of their target career goal.

### Use these rules:

---

## 1. For Software Engineer / Service-Based Roles:
- DSA score ≥ 8 → Highly ready
- 5 ≤ DSA < 8 → Moderately ready
- DSA < 5 → Needs major improvement

Projects also add value:
- Projects ≥ 2 → Good
- Projects < 2 → Weak portfolio

---

## 2. For Startup-Based Roles:
- Skills score ≥ 8 AND Projects ≥ 5 → Highly ready  
- 3 ≤ Projects < 5 → Moderate  
- Projects < 3 → Needs improvement

---

## 3. For Higher Studies:
- Academics ≥ 8 → Strong readiness
- 6–7 → Moderate  
- < 6 → Weak academic readiness

---

### Input Data:

Student profile:
{json.dumps(profile, indent=2)}

Evaluation scores:
{json.dumps(evaluation, indent=2)}

---

### Output Format (STRICT JSON):

{{
  "readiness_level": "Highly Ready / Moderately Ready / Needs Improvement",
  "gaps": {{
    "skills_gap": "text",
    "project_gap": "text",
    "dsa_gap": "text",
    "academic_gap": "text"
  }},
  "final_summary": "one short paragraph describing readiness + gap"
}}
"""

        response = model.generate_content(prompt)

        try:
            clean_output = response.text.strip()
            clean_output = clean_output.replace("```json", "").replace("```", "").strip()
            result = json.loads(clean_output)
        except:
            raise ValueError("LLM did not return clean JSON.\nRaw Output:\n" + response.text)

        return result
