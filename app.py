from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory log storage (can be replaced with a database)
logs = []

# Endpoint to receive log data from the bot
@app.route('/api/logs', methods=['POST'])
def receive_log():
    data = request.get_json()
    
    # Example: Log the action to an in-memory list (can be replaced with a DB)
    logs.append(data)
    print(data)  # Log to console for testing purposes
    
    # Respond with a success message
    return jsonify({"status": "success"}), 200

# Endpoint to retrieve logs (for displaying on your website)
@app.route('/logs', methods=['GET'])
def get_logs():
    # Render logs as a simple JSON response
    return jsonify(logs)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)  # Change the port if needed
