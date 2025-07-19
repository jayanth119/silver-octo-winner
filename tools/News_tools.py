import requests
import os 
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.newspaper4k import Newspaper4kTools
import os
from datetime import date , timedelta
from dotenv import load_dotenv

load_dotenv()
groq_api_key = os.environ.get('GOOGLE_API_KEY')

web_search = DuckDuckGoTools()
newspaper = Newspaper4kTools()
class NewsTools:
    def __init__(self , topic ):
        self.topic = topic
    def get_news_headlines(self) -> list:
        # from_to is less than one month compare to today
        from_to = date.today() - timedelta(days=30)
        
        print(from_to)
        news_api_key = os.environ.get('NEWS_API_KEY')
        url = f"https://newsapi.org/v2/everything?q={self.topic}&from={from_to}&sortBy=popularity&apiKey={ news_api_key }" # "55d9223ae2564088985b9481c336d45d"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            articles = data.get('articles', [])
            extracted = []
            
            # Add stronger filtering to ensure topic relevance
            for article in articles:
                title = article.get('title', '').lower()
                description = article.get('description', '').lower()
                
                # Only include articles that explicitly mention the topic
                if self.topic.lower() in title or self.topic.lower() in description:
                    info = {
                        'title': article.get('title'),
                        'description': article.get('description'),
                        'url': article.get('url'),
                        'urlToImage': article.get('urlToImage'),
                        'publishedAt': article.get('publishedAt')  # Include publish date for sorting
                    }
                    extracted.append(info)
            
            # Sort by date to ensure most recent articles
            extracted.sort(key=lambda x: x.get('publishedAt', ''), reverse=True)
            # print(extracted[:5])
            return extracted[:5]  # Return only the 5 most recent and relevant articles
        except requests.RequestException as e:
            print(f"An error occurred while fetching news headlines: {e}")
            return {"error": "Failed to fetch news headlines."}






