import json
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.googlesearch import GoogleSearchTools
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.models import llm
from prompts.diseasePrompt import disease_info_prompt


class DiseaseAgent:
    def __init__(self):
        self.agent = Agent(
            name="DiseaseAgent",
            model=llm,
            markdown=False,
            tools=[DuckDuckGoTools(), GoogleSearchTools()],
            show_tool_calls=True,
            description=disease_info_prompt
        )

    def get_disease_info(self, disease_name, language="English"):
        try:
            query = f"""
            Provide full health information about the disease: {disease_name}
            Language: {language}
            Return only valid JSON as per the given format.
            """
            response = self.agent.run(query)
            return self.parse_json_response(response.content)
        except Exception as e:
            print(f"Error fetching disease info: {e}")
            return None

    def parse_json_response(self, response_content):
        try:
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
    disease_agent = DiseaseAgent()
    
    disease_name = "Fever" 
    language = "English"      

    result = disease_agent.get_disease_info(disease_name, language)

    print("\n===== Disease Info =====\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))