import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


list1 = [1, 2, 3, 4, 5, 6, 7]
list2 = [5, 4, 2, 8, 9]

numbers = [1, 2]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.H4('Arribades per minut'),
        html.Div(id='text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*250, # in milliseconds
            n_intervals=0
        )
    ])
)



# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):

    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    list1.append(numbers[0])
    numbers[0] = numbers[0] + 1
    list2.append(numbers[1])
    numbers[1] = numbers[1] * 2

    fig.append_trace({
        'x': list1,
        'y': list2,
        'name': 'Altitude',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)

