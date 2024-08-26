import google.generativeai as genai
import os

class Gemini:
    def __init__(self, model_name='gemini-pro') -> None:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
        self.model = genai.GenerativeModel(model_name=model_name)

    def gemini_generate(self, prompt):
        res = self.model.generate_content(prompt)
        try:
            return res.text
        except ValueError:
            return res.candidate.safety_ratings