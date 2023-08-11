from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
import plotly
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import pickle
import requests
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.chat_models import ChatOpenAI
pd.options.plotting.backend = "plotly"

engine = 'Llama'

app = Flask(__name__, static_folder='static')
CORS(app)

regions = ['Asia', 'Europe', 'Africa', 'Hawaiian Region', 'North America']


dataset_name = "temperature anomaly data"
t5_outputs = pickle.load(open('all_t5_outputs_anomaly.p', 'rb')) 

all_text_str = ''
for c in regions:
    all_text_str += '\n ' + t5_outputs[c]

if engine == 'ChatGPT':
    context = SystemMessage(content=all_text_str)
    chat_connect = ChatOpenAI(model_name="gpt-4",
                          temperature=0.3, openai_api_key='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')
elif engine=='Llama':
    context = all_text_str
    api_url = 	'https://1wea2w43if.execute-api.us-east-1.amazonaws.com/default/call-llama'


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/plot')
def plot():
    df = pd.read_csv('TCube/Data/GlobalTemperature/anomalies_our_world_in_data.csv')
    fig = go.Figure()
    for c in regions:
        country_df = df.loc[df['Region']==c]
        country_df['dt']=pd.to_datetime(country_df['dt'])
        # if c == 'United States':
        #     min_year = 1825
        # else:
        #     min_year = 1600

        # rolling_df = (country_df[(country_df['dt'].dt.month<=12) 
        #                         & (country_df['dt'].dt.year>=min_year) 
        #                         & (country_df['dt'].dt.year<=2012)]
        # .groupby(country_df['dt'].dt.year)[['AverageTemperature']].mean()
        # .rolling(10).mean()
        # .dropna()
        # .reset_index()
        # .rename(columns={'dt':'Year', 
        #                 'AverageTemperature': 'TenYearAverageTemperature'}))
        fig.add_trace(
            go.Scatter(
                    x=country_df['Year'],
                    y=country_df['Anomaly'],
                    mode='lines',
                    name=c,
                    # Legend will use this name
            )
        )

        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Temperature Anomaly (\u00B0C)',
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

#ChatGPT
# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.get_json()
#     message = data.get('message')
#     print(message)
#     messages = [
#                 context,
#                 HumanMessage(content=message)
#             ]
    
#     response=chat_connect(messages)
#     print(response)

#     return jsonify(reply=response.content)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message')
    print(context)
    if engine == 'ChatGPT':
        messages = [
                context,
                HumanMessage(content=message)
            ]
        response = chat_connect(messages)
        return jsonify(reply=response.content)
    
    elif engine == 'Llama':
        json_body = {
        "inputs": [
        [
            {"role": "system", "content": f"You are DataArticles. You generate texts to help journalists write stories about data. The data you are writing about today is {dataset_name}. Here is information about the data: {context}"},
            {"role": "user", "content": ""}, # have to call user before assistant for api to work
            {"role": "assistant", "content": context},
            {"role": "user", "content": message}
        ]
        ],
        "parameters": {"max_new_tokens":1024, "top_p":0.9, "temperature":0.6}
        }
        r = requests.post(api_url, json=json_body)

        return jsonify(reply=r.json()[0]['generation']['content'])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')