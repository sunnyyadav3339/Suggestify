from flask import Flask, request, jsonify
from flask_cors import CORS
from mira_sdk import MiraClient

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Initialize Mira Client
client = MiraClient(config={"API_KEY": "sb-d51ccac8048865dde9809141771c8e3d"})

@app.route('/get-recommendations', methods=['POST'])
def get_recommendations():
    # Log the incoming data for debugging
    print("Received data:", request.json)
    
    genre = request.json.get('genre')
    description = request.json.get('description')

    if not genre or not description:
        return jsonify({"error": "Please provide both genre and description."}), 400

    input_data = {
        "genre": genre,
        "description": description
    }

    version = "1.0.0"
    flow_name = f"@dhruv/movie-recommender/{version}"

    try:
        result = client.flow.execute(flow_name, input_data)
        return jsonify({"recommendations": result})
    except Exception as e:
        print(f"Error executing flow: {e}")
        return jsonify({"error": f"Failed to fetch recommendations: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
