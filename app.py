from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
import plotly
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
pd.options.plotting.backend = "plotly"

app = Flask(__name__, static_folder='static')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/plot')
def plot():
    df = pd.read_csv('TCube/Data/GlobalTemperature/GlobalLandTemperaturesByCountry.csv')
    #countries = ['United States', 'United Kingdom', 'France', 'Spain', 'Italy', 'Germany', 'Russia']
    countries = ['United States', 'United Kingdom', 'Germany']
    fig = go.Figure()
    for c in countries:
        country_df = df.loc[df['Country']==c]
        country_df['dt']=pd.to_datetime(country_df['dt'])
        rolling_df = (country_df[(country_df['dt'].dt.month<=12) 
                                & (country_df['dt'].dt.year>=1825) 
                                & (country_df['dt'].dt.year<=2012)]
        .groupby(country_df['dt'].dt.year)[['AverageTemperature']].mean()
        .rolling(10).mean()
        .dropna()
        .reset_index()
        .rename(columns={'dt':'Year', 
                        'AverageTemperature': 'TenYearAverageTemperature'}))
        fig.add_trace(
            go.Scatter(
                    x=rolling_df['Year'],
                    y=rolling_df['TenYearAverageTemperature'],
                    mode='lines',
                    name=c,
                    # Legend will use this name
            )
        )

        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Temperature',
            legend_title='',
            autosize=True,
            height=400,
            font=dict(
                family="Open Sans, arial",
                size=14,  # Set the font size here
                color='darkslategray',
                ),
            legend=dict(
                y=0.5,
                traceorder='reversed',
                font=dict(
                    size=16
                )
            ),
            template='simple_white'
        )
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