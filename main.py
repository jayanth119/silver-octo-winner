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
cors = CORS(app , resources={r"/*": {"origins": "*"}})
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
    # Get the blog post, which is now a dictionary with 'title' and 'blog_post'
    final_post = BlogAgent().runagent()
    # Directly return the result as JSON
    return jsonify({"status": "success", "blog_post": final_post['blog_post'] , "title": final_post['title']})

    
    return {"status": "success", "blog_post": final_post, "title": title}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
