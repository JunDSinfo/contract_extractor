import time

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import google.generativeai as genai
import os

#
# generation_config = {
#   "temperature": 0.9,
#   "top_p": 1,
#   "top_k": 1,
#   "max_output_tokens": 2048,
# }
#
# safety_settings = [
#   {
#     "category": "HARM_CATEGORY_HARASSMENT",
#     "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#   },
#   {
#     "category": "HARM_CATEGORY_HATE_SPEECH",
#     "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#   },
#   {
#     "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
#     "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#   },
#   {
#     "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
#     "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#   }
# ]

class Auditor:
    def __init__(self,prompt, api_key=os.getenv("GOOGLE_API_KEY")):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-pro')
        self.prompt = prompt

    def get_gemini_response(self, doc):

        response = self.model.generate_content([doc, self.prompt])
        return response.text
class TaskAuditor(Auditor):
    def __init__(self,prompt):
        super().__init__(prompt)
    def get_response(self, doc):
        return self.get_gemini_response(doc)


class TermAuditor(Auditor):
    def __init__(self,prompt):
        super().__init__(prompt)
    def get_response(self, doc):
        return self.get_gemini_response(doc)
class Analyzer(Auditor):
    def __init__(self, prompt):
        super().__init__(prompt)
        self.chat = self.model.start_chat()
        self.chat.send_message(prompt)

    def analyze(self, task):
        time.sleep(5)
        self.chat.send_message(task)
        result = self.chat.last.text
        return result



