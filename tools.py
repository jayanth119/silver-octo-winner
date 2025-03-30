import requests
import os 
import json
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.google import Gemini
from agno.tools.newspaper4k import Newspaper4kTools
from agno.agent import Agent
import os
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.environ.get('GOOGLE_API_KEY')

web_search = DuckDuckGoTools()
newspaper = Newspaper4kTools()
class NewsTools:
    def __init__(self , topic ):
        self.topic = topic
    def get_news_headlines(self ) -> list:
        """
        This function fetches the latest news headlines from a news API.
        It returns a list of dictionaries containing the title, description, URL, and image URL for each article.
        """
        # Define the API endpoint. Replace YOUR_API_KEY with your actual API key.
        from_to = "2025-03-28"
        to = "2025-03-28"
        url = f"https://newsapi.org/v2/everything?q={self.topic}&from={from_to}&to={to}&sortBy=popularity&apiKey=55d9223ae2564088985b9481c336d45d"     
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses

            # Parse the JSON response
            # Using response.json() directly since response is not a string.
            data = response.json()  
            
            articles = data.get('articles', [])
            extracted = []
        
            for article in articles:
                info = {
                    'title': article.get('title'),
                    'description': article.get('description'),
                    'url': article.get('url'),
                    'urlToImage': article.get('urlToImage')
                }
                extracted.append(info)
            return extracted
        except requests.RequestException as e:
            print(f"An error occurred while fetching news headlines: {e}")
            return {"error": "Failed to fetch news headlines."}






