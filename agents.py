import os
import random
import json
import markdown  # Ensure you have the 'markdown' package installed (pip install markdown)
from textwrap import dedent
from dotenv import load_dotenv
import mistune
# Import required tools and models
from agno.models.google import Gemini
from agno.agent import Agent
from tools import NewsTools, web_search, newspaper
from models import llm

# Load environment variables
load_dotenv()
groq_api_key = os.environ.get('GOOGLE_API_KEY')


class NewsAgent:
    """
    This agent selects a random topic, retrieves news headlines using NewsTools,
    and then calls an agent to fetch the latest relevant news content.
    """
    def runagent(self):
        topics = ["kafka", "python", "java"]
        topic = random.choice(topics)
        print(f"Selected topic: {topic}")
        news_headlines = NewsTools(topic).get_news_headlines()
        
        news_agent = Agent(
            description=dedent("""\
                You are BlogResearch of admin (jayanth), an elite research assistant specializing in discovering
                high-quality sources for compelling blog content. Your expertise includes:
                - Finding authoritative and trending sources
                - Evaluating content credibility and relevance
                - Identifying diverse perspectives and expert opinions
                - Discovering unique angles and insights
                - Ensuring comprehensive topic coverage
            """),
            instructions=dedent("""\
                1. Search Strategy 🔍
                   - Find 10-15 relevant sources and select the 5-7 best ones.
                   - Prioritize recent, authoritative content.
                   - Look for unique angles and expert insights.
                2. Source Evaluation 📊
                   - Verify source credibility and expertise.
                   - Check publication dates for timeliness.
                   - Assess content depth and uniqueness.
                3. Diversity of Perspectives 🌐
                   - Include different viewpoints.
                   - Gather both mainstream and expert opinions.
                   - Find supporting data and statistics.
            """),
            model=llm,
            show_tool_calls=True,
            markdown=True,
            tools=[web_search],
        )
        response = news_agent.run(
            f"Get the latest news about {news_headlines}. It should include complete information and insights on the topic from recent times."
        )
        return response.content


class ResearchAgent:
    """
    This agent takes the news content from NewsAgent, extracts the detailed content,
    and processes it into a clean markdown format for blog creation.
    """
    def runagent(self):
        news_content = NewsAgent().runagent()
        researcher_agent = Agent(
            description=dedent("""\
                You are ContentBot of admin (jayanth), a specialist in extracting and processing digital content
                for blog creation. Your expertise includes:
                - Efficient content extraction
                - Smart formatting and structuring
                - Key information identification
                - Quote and statistic preservation
                - Maintaining source attribution
            """),
            instructions=dedent("""\
                1. Content Extraction 📑
                   - Extract content from the article.
                   - Preserve important quotes and statistics.
                   - Maintain proper attribution.
                   - Handle paywalls gracefully.
                2. Content Processing 🔄
                   - Format text in clean markdown.
                   - Preserve key information.
                   - Structure content logically.
                3. Quality Control ✅
                   - Verify content relevance.
                   - Ensure accurate extraction.
                   - Maintain readability.
            """),
            model=llm,
            show_tool_calls=True,
            markdown=True,
            tools=[newspaper],
        )
        response = researcher_agent.run(
            f"Get the complete information about the following content: {news_content}. It should include all necessary details about the topic."
        )
        return response.content


class BlogAgent:
    """
    This agent takes the processed content from ResearchAgent and crafts a fully structured,
    SEO-friendly blog post complete with introduction, body, and conclusion.
    """
    def runagent(self):
        research_content = ResearchAgent().runagent()
        blog_agent = Agent(
            description=dedent("""\
                You are BlogMaster(name epsilon ), an elite content creator combining journalistic excellence
                with digital marketing expertise. Your strengths include:
                - Crafting viral-worthy headlines
                - Writing engaging introductions
                - Structuring content for digital consumption
                - Incorporating research seamlessly
                - Optimizing for SEO while maintaining quality
                - Creating shareable conclusions
            """),
            instructions=dedent("""\
                You are a blog writer AI working on behalf of admin (jayanth). your  name is Epsilon.
                Please include an introduction that presents admin and yourself, greet the readers,
                and then write a blog post on the given topic. The post must have an introduction,
                body, and conclusion. Ensure the post is informative, engaging, easy to understand,
                and covers all points from the starting to ending positions.
                
                1. Content Strategy 📝
                   - Craft attention-grabbing headlines.
                   - Write compelling introductions.
                   - Structure content for engagement.
                   - Include relevant subheadings.
                2. Writing Excellence ✍️
                   - Balance expertise with accessibility.
                   - Use clear, engaging language.
                   - Include relevant examples.
                   - Incorporate statistics naturally.
                3. Source Integration 🔍
                   - Cite sources properly.
                   - Include expert quotes.
                   - Maintain factual accuracy.
                4. Digital Optimization 💻
                   - Structure for scanability.
                   - Include shareable takeaways.
                   - Optimize for SEO.
                   - Add engaging subheadings.
            """),
            model=llm,
            show_tool_calls=True,
            markdown=True,
        )
        response = blog_agent.run(
            f"Write a blog post about the following content: {research_content}"
        )
        md_converter = mistune.create_markdown()
        html_post = md_converter(response.content)
        return html_post
        


if __name__ == "__main__":
    final_post = BlogAgent().runagent()
    # Convert the generated Markdown blog post to HTML
    html_post = markdown.markdown(final_post)
    prin
    # Create a JSON response with the HTML formatted blog post
    # json_response = {
    #     "status": "success",
    #     "blog_post": html_post
    # }
    # print(json.dumps(json_response, indent=4))
