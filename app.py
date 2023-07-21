from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
import plotly
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import pickle
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI
pd.options.plotting.backend = "plotly"

app = Flask(__name__, static_folder='static')
CORS(app)

t5_outputs = pickle.load(open('all_t5_outputs.p', 'rb')) 
countries = ['Germany', 'United Kingdom', 'United States']

all_text_str = ''
for c in countries:
    all_text_str += '\n ' + t5_outputs[c]

context = SystemMessage(content=all_text_str)
chat_connect = ChatOpenAI(model_name="gpt-3.5-turbo",
                          temperature=0.3, openai_api_key='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')

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
        if c == 'United States':
            min_year = 1825
        else:
            min_year = 1600

        rolling_df = (country_df[(country_df['dt'].dt.month<=12) 
                                & (country_df['dt'].dt.year>=min_year) 
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
            yaxis_title='"Temperature (\u00B0C)',
            legend_title='',
            autosize=True,
            height=450,
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
    print(message)
    messages = [
                context,
                HumanMessage(content=message)
            ]
    
    response=chat_connect(messages)
    print(response)

    return jsonify(reply=response.content)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')