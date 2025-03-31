import os
import random
import json
import mistune  # Alternative Markdown parser
from textwrap import dedent
from dotenv import load_dotenv
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
        topics = ["kafka", "python", "java" , "programming" , "data science" , "AI" , "ML" , "DL" , "NLP" , "cloud computing" , "web development", "latest tech news ", "new technology", "latest news", "latest updates", "latest trends" , "latest news in technology", "latest news in AI", "latest news in ML", "latest news in DL", "latest news in NLP", "latest news in cloud computing", "latest news in web development" , "new models in generative ai ", "latest news in generative ai" , "latest news in data science" , "latest news in programming" , "latest news in java" , "latest news in python"] 
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
            f"Get the latest news about {topic }. It should include complete information and insights on the topic from recent times."
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
        # topics = ["kafka", "python", "java" , "programming" , "data science" , "AI" , "ML" , "DL" , "NLP" , "cloud computing" , "web development", "latest tech news ", "new technology", "latest news", "latest updates", "latest trends" , "latest news in technology", "latest news in AI", "latest news in ML", "latest news in DL", "latest news in NLP", "latest news in cloud computing", "latest news in web development" , "new models in generative ai ", "latest news in generative ai" , "latest news in data science" , "latest news in programming" , "latest news in java" , "latest news in python"] 
        # topic = random.choice(topics)
        response = researcher_agent.run(
            f"Get the complete information about the following content: {news_content} . It should include all necessary details about the topic."
        )
        return response.content


class BlogAgent:
    """
    This agent takes the processed content from ResearchAgent and crafts a fully structured,
    SEO-friendly blog post complete with a dynamic title, introduction, body, and conclusion.
    The blog post is short, crisp, strictly on topic, and includes no deviations.
    """
    def runagent(self):
        research_content = ResearchAgent().runagent()
        blog_agent = Agent(
            description=dedent("""\
                You are BlogMaster (name: Epsilon), an elite content creator combining journalistic excellence
        
                with digital marketing expertise. Your strengths include:
                - Crafting viral-worthy headlines
                - Writing engaging introductions
                - Structuring content for digital consumption
                - Incorporating research seamlessly
                - Optimizing for SEO while maintaining quality
                - Creating shareable conclusions
            """),
            instructions=dedent("""\
                You are a blog writer AI working on behalf of admin (jayanth) and your name is Epsilon.
                provide the title for the blog post at the starting with # name of the title. 
                Introduce your self as Epsilon and explain your purpose.
                Using the provided content, write a short and crisp blog post that is strictly related to the topic.
                Do not deviate from the topic. The blog post must start with a dynamic title on the first line 
                using Markdown syntax (e.g., "# Your Dynamic Title"). Following the title, include an introduction, 
                a concise body, and a conclusion.
            """),
            model=llm,
            show_tool_calls=True,
            markdown=True,
        )
        # topics = ["kafka", "python", "java" , "programming" , "data science" , "AI" , "ML" , "DL" , "NLP" , "cloud computing" , "web development", "latest tech news ", "new technology", "latest news", "latest updates", "latest trends" , "latest news in technology", "latest news in AI", "latest news in ML", "latest news in DL", "latest news in NLP", "latest news in cloud computing", "latest news in web development" , "new models in generative ai ", "latest news in generative ai" , "latest news in data science" , "latest news in programming" , "latest news in java" , "latest news in python"] 
        # topic = random.choice(topics)
        response = blog_agent.run(
            f"Write a blog post about the following content: {research_content}."
        )
        
        # The response is in Markdown format; now extract the dynamic title and content.
        markdown_content = response.content
        
        # Split the Markdown by lines
        lines = markdown_content.splitlines()
        dynamic_title = "Untitled Blog Post" + " (Epsilon)"
        content_lines = []
        if lines and lines[0].startswith("# "):
            dynamic_title = lines[0][2:].strip()  # Remove "# " from the title line
            content_lines = lines[1:]
        else:
            content_lines = lines
        
        # Join the remaining lines to form the blog content markdown
        blog_markdown_content = "\n".join(content_lines)
        
        # Convert the Markdown content (excluding the title) to HTML using Mistune
        md_converter = mistune.create_markdown()
        html_post = md_converter(blog_markdown_content)
        
        # Return both the dynamic title and HTML blog post
        return {"title": dynamic_title, "blog_post": html_post}


if __name__ == "__main__":
    final_output = BlogAgent().runagent()
    # Print the final output as a JSON formatted string
    print(json.dumps(final_output, indent=4))
