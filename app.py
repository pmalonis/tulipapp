from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message')

    # TODO: Handle the message and generate a response.
    # This could involve calling a function that generates a response based on the message.
    # For now, we'll just echo the user's message back to them.

    response = 'You said: ' + message
    return jsonify(reply=response)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')