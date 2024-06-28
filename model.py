from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import google.generativeai as genai
import os




class Auditor:
    def __init__(self, api_key=os.getenv("GOOGLE_API_KEY")):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-pro')
    def get_model(self):
        return self.model



