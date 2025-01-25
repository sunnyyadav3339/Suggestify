from flask import Flask, request, jsonify
from flask_cors import CORS
from mira_sdk import MiraClient

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Initialize Mira Client
client = MiraClient(config={"API_KEY": "sb-d51ccac8048865dde9809141771c8e3d"})  # Replace with your actual API key

@app.route('/find-laptop', methods=['POST'])
def find_laptop():
    # Log the incoming data for debugging
    print("Received data:", request.json)
    
    price = request.json.get('price')
    yes_or_no = request.json.get('yesOrNo')

    if not price or not yes_or_no:
        return jsonify({"error": "Please provide both price and yesOrNo."}), 400

    input_data = {
        "price": price,
        "yesOrNo": yes_or_no
    }

    version = "1.0.0"
    flow_name = f"@hamiz/laptop-finder-budget/{version}"

    try:
        result = client.flow.execute(flow_name, input_data)
        return jsonify({"laptopRecommendations": result})
    except Exception as e:
        print(f"Error executing flow: {e}")
        return jsonify({"error": f"Failed to fetch recommendations: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)