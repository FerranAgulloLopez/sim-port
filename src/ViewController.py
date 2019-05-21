import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import pandas as pd
from collections import deque
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Auxiliary operations
def parse_time(time):
    hour = int(time/3600)
    minutes = int((time % 3600)/60)
    hourstr = str(hour)
    minutesstr = str(minutes)
    if hour < 10:
        hourstr = '0' + hourstr
    if minutes < 10:
        minutesstr = '0' + minutesstr
    return hourstr + ':' + minutesstr

# Main program

# load trace
df = pd.read_csv("trace.csv")

# general data
mainTime = 6*3600

# data for entries graph
entries = deque([], 60)
entriesTime = deque([], 60)
entriesTimeNames = deque([], 60)

# data for buffer
buffer_max_size = 100
buffer_slots_busy = 0

# data for queue
queue_max_size = 90
queue_slots_busy = 0

# data for processors
processors_max_number = 52
processors_busy = 0

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('Arribades a la terminal (unitat de temps = minuts)'),
        html.Div(id='text'),
        dcc.Graph(id='pie-graph'),
       dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            # each 250 milliseconds represents a minute
            interval=1*250, # in milliseconds
            n_intervals=0
        )
    ])
)

@app.callback([Output('live-update-graph', 'figure'),
               Output('pie-graph', 'figure')],
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    global mainTime, df, entries, entriesTime, buffer_slots_busy, queue_slots_busy, buffer_max_size, queue_max_size, processors_max_number, processors_busy

    mainTime += 60

    entries.append(0)
    entriesTime.append(mainTime)
    entriesTimeNames.append(parse_time(mainTime))
    print(parse_time(mainTime))

    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    correct = True
    size = len(df.index)
    count = 0
    while correct and (count < size):
        event = df.iloc[count]
        if event['Current_Time'] > mainTime:
            correct = False
        else:
            if event['Event_Name'] == 'NEXT_ARRIVAL':
                entries[-1] += 1
                queue_slots_busy = event['Queue_Length']
                processors_busy = event['Service_Processors']
                buffer_slots_busy = event['Buffer_Length']
            count += 1
    df = df.iloc[count:]

    fig['layout']['xaxis'] = {
        'title': 'Temps',
        'ticktext': list(entriesTimeNames),
        'tickvals': list(entriesTime)
    }

    fig.append_trace({
        'x': list(entriesTime),
        'y': list(entries),
        'name': 'Entrades',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': [1, 2, 3, 4, 5],
        'y': [5, 8, 11, 14, 20],
        'name': 'Entrades',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)

    fig2 = {
        "data": [
            {
                "values": [buffer_slots_busy, buffer_max_size-buffer_slots_busy],
                "labels": [
                    "Busy slots",
                    "Free Slots"
                ],
                "domain": {"column": 0},
                "hoverinfo": "label+value+name",
                "hole": .4,
                "type": "pie",
                "title": "Buffer"
            },
            {
                "values": [queue_slots_busy, queue_max_size - queue_slots_busy],
                "labels": [
                    "Busy slots",
                    "Free Slots"
                ],
                "textposition": "inside",
                "domain": {"column": 1},
                "title": "Queue",
                "hoverinfo": "label+value+name",
                "hole": .4,
                "type": "pie"
            },
            {
                "values": [processors_busy, processors_max_number - processors_busy],
                "labels": [
                    "Service-Processors"
                    "Idle-Processors",
                ],
                "textposition": "inside",
                "domain": {"column": 2},
                "title": "Processors",
                "hoverinfo": "label+value+name",
                "hole": .4,
                "type": "pie"
            }
        ],
        "layout": {
            "title": "",
            "grid": {"rows": 1, "columns": 3},
            "annotations": [
                {
                    "font": {
                        "size": 20
                    },
                    "text": "",
                    "showarrow": False,
                    "x": 0.0,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 20
                    },
                    "text": "",
                    "showarrow": False,
                    "x": 0.30,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 20
                    },
                    "text": "",
                    "showarrow": False,
                    "x": 0.6,
                    "y": 0.5
                }
            ]
        }
    }

    return fig2, fig


if __name__ == '__main__':
    app.run_server(debug=True)




