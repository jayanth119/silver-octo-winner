import os
import sys
import json
from agno.agent import Agent
from agno.media import Image
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.googlesearch import GoogleSearchTools

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.models import llm
from prompts.medicinePrompt import medicine_prompt, medicine_info_prompt


class MedicineAgent:
    def __init__(self):
        self.agent = Agent(
            name="MedicineAgent",
            model=llm,
            markdown=False,
            description=medicine_prompt
        )

    def analyze_image(self, img_path):
        try:
            if not os.path.exists(img_path):
                raise FileNotFoundError(f"File not found: {img_path}")

            print(f"Analyzing image: {img_path}")
            image = Image(filepath=img_path)

            response = self.agent.run(
                "Analyze the provided medicine image and extract details as per the given format.",
                images=[image]
            )
            return response.content
        except Exception as e:
            print(f"Error analyzing image: {e}")
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


class MedicineInfoAgent:
    def __init__(self):
        self.agent = Agent(
            name="MedicineInfoAgent",
            model=llm,
            markdown=False,
            tools=[DuckDuckGoTools(), GoogleSearchTools()],
            show_tool_calls=True,
            description=medicine_info_prompt
        )

    def get_medicine_info(self, medicine_name, language="English"):
        try:
            query = f"""
            Provide full information about the medicine: {medicine_name}
            Language: {language}
            Return only valid JSON as per the given format.
            """
            response = self.agent.run(query)
            return response.content
        except Exception as e:
            print(f"Error fetching medicine info: {e}")
            return None


class MedicinePipeline:
    def __init__(self):
        self.extractor = MedicineAgent()
        self.info_agent = MedicineInfoAgent()

    def process(self, img_path, language="English"):
        print("Step 1: Extracting medicine details from image...")
        raw_response = self.extractor.analyze_image(img_path)

        if not raw_response:
            return "Failed to extract medicine info from image."

        parsed_data = self.extractor.parse_json_response(raw_response)
        if not parsed_data:
            return "Failed to parse extracted medicine details."

        if isinstance(parsed_data, list):
            medicine_names = [item.get("medicine_name", "") for item in parsed_data if item.get("medicine_name")]
        else:
            medicine_names = [parsed_data.get("medicine_name", "")]

        if not medicine_names:
            return "No medicine names found in image."

        print(f"Step 2: Fetching detailed info in {language}...")
        results = []
        for med in medicine_names:
            details = self.info_agent.get_medicine_info(med, language)
            parsed_details = self.extractor.parse_json_response(details)
            if parsed_details:
                results.append(parsed_details)

        return results




if __name__ == "__main__":
    pipeline = MedicinePipeline()
    image_path = "/Users/jayanth/Documents/GitHub/silver-octo-winner/data"
    language = "English"  

    result = pipeline.process(image_path, language)

    print("\n===== Final Output =====\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
