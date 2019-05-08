import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import pandas as pd
from collections import deque
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# load trace
df = pd.read_csv("trace.csv")

# general data
mainTime = 6*3600

# data for entries graph
entries = deque([], 60)
entriesTime = deque([], 60)

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('Arribades a la terminal (unitat de temps = minuts)'),
        html.Div(id='text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            # each 250 milliseconds represents a minute
            interval=1*250, # in milliseconds
            n_intervals=0
        )
    ])
)

@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    global mainTime, df, entries, entriesTime

    mainTime += 60
    entries.append(0)
    entriesTime.append(mainTime)

    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    correct = True
    size = len(df.index)
    print(size)
    count = 0
    while correct and (count < size):
        event = df.iloc[count]
        if event['Current_Time'] > mainTime:
            correct = False
        else:
            if event['Event_Name'] == 'NEXT_ARRIVAL':
                entries[-1] += 1
            count += 1
    df = df.iloc[count:]

    fig.append_trace({
        'x': list(entriesTime),
        'y': list(entries),
        'name': 'Entrades',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)


# Auxiliary operations



