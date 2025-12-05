import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

class ProfileCollectorAgent:
    def __init__(self, model):
        self.model = model

    def collect(self, user_input):
        prompt = f"""
        Extract the following fields from the user's message:

        - name
        - cgpa (0-10)
        - skills (list)
        - projects (list)
        - competitive programming experience
        - career goal
        - No. of DSA solved
        - No. of interships

        If any field is missing, write "missing".
        Only return valid JSON.

        User Input:
        {user_input}
        """

        response = self.model.generate_content(prompt)
        return response.text
