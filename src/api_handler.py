import google.generativeai as genai
import json
from .config import GEMINI_API_KEY, TREATMENT_PLANS

class GeminiHandler:
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-pro')
        else:
            self.model = None

    def get_treatment_plan(self, disease_name):
        if not self.model: return TREATMENT_PLANS['Fallback']

        prompt = f"""
        You are an elite agricultural expert and botanist. Provide a highly comprehensive and detailed treatment plan for the corn disease: "{disease_name}".
        Return the response strictly as a JSON object with the following keys exactly:
        - name: The common name of the disease.
        - scientific_name: The scientific name of the pathogen.
        - symptoms: In-depth description of visual symptoms and how to identify them early.
        - prevention: Step-by-step preventative agronomic practices.
        - organic: Specific organic/biological control methods (include mixtures if applicable).
        - chemical: Specific synthetic chemical controls (include active ingredients and application timing).
        Do not include markdown formatting like ```json ... ```. Just the raw JSON.
        """
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[len("```json"):].strip()
            if text.endswith("```"):
                text = text[:-len("```")].strip()
            return json.loads(text)
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            return TREATMENT_PLANS['Fallback']