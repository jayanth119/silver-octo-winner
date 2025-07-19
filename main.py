from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
import os 
import sys 
import tempfile
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.news_agents import BlogAgent 
from agents.medicine_agents import MedicinePipeline
from agents.diseases_agents import DiseaseAgent
from agents.doctor_agents import DoctorAgent 
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
    final_post = BlogAgent().runagent()
    return jsonify({"status": "success", "blog_post": final_post['blog_post'] , "title": final_post['title']})


@app.route('/api/chat', methods=["POST"])
def get_chat():
    try:
        # Get user input from request
        user_query = request.form.get("query", None)

        if not user_query:
            return jsonify({"status": "error", "message": "Query is required"}), 400

        # Initialize Doctor Agent
        doctor = DoctorAgent()

        # Get response from the agent
        raw_response = doctor.chat(user_query)

        # Handle response (ensure JSON-safe)
        if isinstance(raw_response, str):
            response = raw_response
        elif isinstance(raw_response, dict):
            response = raw_response
        else:
            response = str(raw_response)

        return jsonify({
            "status": "success",
            "query": user_query,
            "response": response
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/api/diseases', methods=["POST"])
def get_disease():
    try:
        # Get data from request
        disease_name = request.form.get("disease_name", None)
        language = request.form.get("language", "English")

        if not disease_name:
            return jsonify({"status": "error", "message": "Disease name is required"}), 400

        # Initialize Disease Agent
        disease_agent = DiseaseAgent()
        raw_response = disease_agent.get_disease_info(disease_name, language)

        # Handle response
        if isinstance(raw_response, str):
            try:
                result = json.loads(raw_response)
            except json.JSONDecodeError:
                result = {"error": "Invalid JSON from AI", "raw_response": raw_response}
        elif isinstance(raw_response, dict):
            result = raw_response
        else:
            result = {"error": "Unknown response type", "raw_response": str(raw_response)}

        return jsonify({
            "status": "success",
            "data": result
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500



@app.route('/api/medicine', methods=["POST"])
def get_medicine():
    try:
        if 'photo' not in request.files:
            return jsonify({"status": "error", "message": "No photo uploaded"}), 400

        photo = request.files['photo']
        if photo.filename == '':
            return jsonify({"status": "error", "message": "Empty file name"}), 400

        language = request.form.get("language", "English")

        # Create a temporary directory for the file
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, photo.filename)
        photo.save(temp_path)

        # Process with pipeline
        pipeline = MedicinePipeline()
        result = pipeline.process(temp_path, language)

        # Delete the file after processing
        os.remove(temp_path)

        return jsonify({
            "status": "success",
            "data": result
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
