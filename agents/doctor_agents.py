import os
import sys
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.models import llm
from prompts.doctorPrompt import doctor_agent_prompt
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.googlesearch import GoogleSearchTools

class DoctorAgent:
    def __init__(self):
        self.agent = Agent(
            name="DoctorAgent",
            model=llm,
            markdown=False,
            description=doctor_agent_prompt,
            tools=[
                DuckDuckGoTools(),
                GoogleSearchTools(),
            ]
        )

    def chat(self, user_message, language="English"):
        try:
            query = f"""
            Language: {language}
            User Question: {user_message}
            Return only valid JSON as per schema.
            """
            response = self.agent.run(query)
            return self.parse_json_response(response.content)
        except Exception as e:
            print(f"Error in DoctorAgent chat: {e}")
            return None

    def parse_json_response(self, response_content):
        """
        Extracts and parses JSON from model output.
        """
        try:
            # Remove markdown if present
            if "```json" in response_content:
                start = response_content.find("```json") + 7
                end = response_content.find("```", start)
                json_str = response_content[start:end].strip()
            elif "```" in response_content:
                start = response_content.find("```") + 3
                end = response_content.find("```", start)
                json_str = response_content[start:end].strip()
            else:
                json_str = response_content.strip()

            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response content: {response_content}")
            return None

if __name__ == "__main__":
    doctor = DoctorAgent()

    response1 = doctor.chat("What is diabetes?")
    print(json.dumps(response1, indent=2, ensure_ascii=False))

    response2 = doctor.chat("What foods should I eat?")
    print(json.dumps(response2, indent=2, ensure_ascii=False))
