from flask import Flask, request, jsonify
from flask_cors import CORS
from mira_sdk import MiraClient

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Initialize Mira Client
client = MiraClient(config={"API_KEY": "sb-d51ccac8048865dde9809141771c8e3d"})

@app.route('/get-music-recommendations', methods=['POST'])
def get_music_recommendations():
    # Log the incoming data for debugging
    print("Received data:", request.json)
    
    mood = request.json.get('Mood')
    language = request.json.get('Language')
    favorite_artist = request.json.get('Favorite Artist')

    if not mood or not language or not favorite_artist:
        return jsonify({"error": "Please provide Mood, Language, and Favorite Artist."}), 400

    input_data = {
        "Mood": mood,
        "Language": language,
        "Favorite Artist": favorite_artist
    }

    version = "1.0.0"
    flow_name = f"@shricharan/music-recommender/{version}"

    try:
        result = client.flow.execute(flow_name, input_data)
        return jsonify({"recommendations": result})
    except Exception as e:
        print(f"Error executing flow: {e}")
        return jsonify({"error": f"Failed to fetch recommendations: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
