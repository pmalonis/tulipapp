from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
import plotly
import plotly.express as px
import pandas as pd

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/plot')
def plot():
   
   # Students data available in a list of list
    students = [['Akash', 34, 'Sydney', 'Australia'],
                ['Rithika', 30, 'Coimbatore', 'India'],
                ['Priya', 31, 'Coimbatore', 'India'],
                ['Sandy', 32, 'Tokyo', 'Japan'],
                ['Praneeth', 16, 'New York', 'US'],
                ['Praveen', 17, 'Toronto', 'Canada']]
     
    # Convert list to dataframe and assign column values
    df = pd.DataFrame(students,
                      columns=['Name', 'Age', 'City', 'Country'],
                      index=['a', 'b', 'c', 'd', 'e', 'f'])
     
    # Create Bar chart
    fig = px.bar(df, x='Name', y='Age', color='City', barmode='group')
     
    # Create graphJSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
     
    # Use render_template to pass graphJSON to html
    return render_template('plot.html', graphJSON=graphJSON)

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