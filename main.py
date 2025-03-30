import os
import random
import mistune  # Alternative Markdown parser
from textwrap import dedent
from dotenv import load_dotenv
from flask import Flask, jsonify
from agents import BlogAgent  # Ensure your agents module is in your PYTHONPATH
from flask_cors import CORS, cross_origin
# Load environment variables
load_dotenv()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_EXPOSE_HEADERS'] = 'Content-Type'
app.config['CORS_ALLOW_HEADERS'] = 'Content-Type'
app.config['CORS_ALLOW_CREDENTIALS'] = True
app.config['CORS_SUPPORTS_CREDENTIALS'] = True
app.config['CORS_ORIGINS'] = '*'

@app.route("/")
def index():
    return jsonify({"Hello": "World"})

@app.route("/blog", methods=["GET"])
def get_blog_post():
    """
    Endpoint to generate and return the blog post as HTML in a JSON response.
    """
    # Generate Markdown blog post using BlogAgent
    final_post = BlogAgent().runagent()
    
    # Convert Markdown to HTML using Mistune
    # md_converter = mistune.create_markdown()
    # html_post = md_converter(final_post)
    
    return jsonify({"status": "success", "blog_post": final_post})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
