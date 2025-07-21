import time
from agno.models.google import Gemini
from dotenv import load_dotenv
import os

load_dotenv()
groq_api_key = os.environ.get('GOOGLE_API_KEY')

def get_llm_instance(max_retries=5):
    attempt = 0
    while attempt < max_retries:
        try:
            llm = Gemini(id="gemini-2.5-flash", api_key=groq_api_key)
            return llm
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}. Retrying in {2**attempt} seconds...")
            time.sleep(2**attempt)
            attempt += 1
    raise Exception("Failed to instantiate Gemini after several attempts")

llm = get_llm_instance()
