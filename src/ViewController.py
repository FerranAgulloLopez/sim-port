from collections import deque

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from src.Charts import Charts
from src.Parameters import Parameters
from src.Constants import Constants

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# Auxiliary operations
def parse_time(time):
    hour = int(time / 3600)
    minutes = int((time % 3600) / 60)
    hourstr = str(hour)
    minutesstr = str(minutes)
    if hour < 10:
        hourstr = '0' + hourstr
    if minutes < 10:
        minutesstr = '0' + minutesstr
    return hourstr + ':' + minutesstr


# Main program

# load traces
df = pd.read_csv(Constants.OUTPUT_PATH + "/trace.csv")
ds = pd.read_csv(Constants.OUTPUT_PATH + "/trace.stats.csv")
parameters = Parameters()
charts = Charts()

if len(df.index) == 0:
    raise Exception("The trace file is empty")

shifts = True
event = df.iloc[0]
if event['Shift'] == '-':
    shifts = False


######################################################### timeline chart

total_time_cargas = 0
total_time_descargas = 0
total_time_duo = 0
service_processors_cargas = 0
service_processors_descargas = 0
service_processors_duo = 0

data_timeline = ds.iloc[0]
timeline_cargas = [None] * 26
timeline_descargas = [None] * 26
timeline_duo = [None] * 26
phases = [None] * 26
count = 2
aux_time = 6
if shifts:
    while (count < len(data_timeline)):
        phase = data_timeline[count]
        hours = data_timeline[count+1]
        aux_service = data_timeline[count+2]
        if aux_service > 100:
            aux_service = 100
        if (phase == 'ENTREGA'):
            total_time_descargas += hours
            service_processors_descargas += hours*aux_service/100
            for i in range(aux_time,aux_time+hours+1):
                timeline_descargas[i] = i
                if i < aux_time+hours:
                    phases[i] = 'ENTREGA'
        if (phase == 'RECOGIDA'):
            total_time_cargas += hours
            service_processors_cargas += hours * aux_service / 100
            for i in range(aux_time,aux_time+hours+1):
                timeline_cargas[i] = i
                if i < aux_time+hours:
                    phases[i] = 'RECOGIDA'
        if (phase == 'DUAL'):
            total_time_duo += hours
            service_processors_duo += hours * aux_service / 100
            for i in range(aux_time,aux_time+hours+1):
                timeline_duo[i] = i
                if i < aux_time+hours:
                    phases[i] = 'DUAL'
        aux_time += hours
        count += 3
timeline_cargas = timeline_cargas[6:21]
timeline_descargas = timeline_descargas[6:21]
timeline_duo = timeline_duo[6:21]
phases = phases[0:20]

total_time_total = 14
service_processors_total = (data_timeline['Processors_Capacity_Used']/100)*total_time_total

######################################################### summary graphs


entries_carregues = 0
entries_descarregues = 0
entries_duo = 0
entries_total = 0

max_queue_carregues = 0
max_queue_descarregues = 0
max_queue_duo = 0
max_queue_total = 0
max_par_carregues = 0
max_par_descarregues = 0
max_par_duo = 0
max_par_total = 0

size = len(df.index)
count = 0

while (count < size):
    event = df.iloc[count]
    event_time = event['Current_Time']
    hour = int(event_time/3600)
    if hour < len(phases):
        phase = phases[hour]
    else:
        phase = phases[-1]
    aux_num_queue = event['Buffer_Length']
    aux_num_par = event['Queue_Length']
    if (phase == 'ENTREGA'):
        if event['Event_Name'] == 'NEXT_ARRIVAL':
            entries_descarregues += 1
        if aux_num_queue > max_queue_descarregues:
            max_queue_descarregues = aux_num_queue
        if aux_num_par > max_par_descarregues:
            max_par_descarregues = aux_num_par
    if (phase == 'RECOGIDA'):
        if event['Event_Name'] == 'NEXT_ARRIVAL':
            entries_carregues += 1
        if aux_num_queue > max_queue_carregues:
            max_queue_carregues = aux_num_queue
        if aux_num_par > max_par_carregues:
            max_par_carregues = aux_num_par
    if (phase == 'DUAL'):
        if event['Event_Name'] == 'NEXT_ARRIVAL':
            entries_duo += 1
        if aux_num_queue > max_queue_duo:
            max_queue_duo = aux_num_queue
        if aux_num_par > max_par_duo:
            max_par_duo = aux_num_par
    if (phase == None):
        if event['Event_Name'] == 'NEXT_ARRIVAL':
            entries_total += 1
        if aux_num_queue > max_queue_total:
            max_queue_total = aux_num_queue
        if aux_num_par > max_par_total:
            max_par_total = aux_num_par
    count += 1

#########################################################




######################################################### dynamic graphs
# general data
mainTime = 6 * 3600
old_event_time = mainTime

# data for entries graph
totalEntities = deque([], 60)
entries = deque([], 60)
entriesTime = deque([], 60)
entriesTimeNames = deque([], 60)

totalEntities.append(0)
entries.append(0)
entriesTime.append(0)
entriesTimeNames.append(0)

# data for buffer
buffer_max_size = 100
buffer_slots_busy = 0

# data for queue
queue_max_size = 90
queue_slots_busy = 0

# data for processors
processors_max_number = 52
processors_free = 0

#########################################################

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    html.Div([
        html.Div([
            html.Span("Simulació del port de Barcelona", className='app-title'),
        ],
            className="row header"
        ),
        html.Div([
            dcc.Tabs(
                id="tabs",
                style={"height": "20", "verticalAlign": "middle"},
                children=[
                    dcc.Tab(label="Real-time simulation", value="real_time_tab", children=[
                        html.Div([
                            dcc.Graph(id='time-graph'),
                            dcc.Graph(id='pie-graph'),
                            dcc.Graph(id='live-update-graph'),
                            dcc.Interval(
                                id='interval-component',
                                # each 250 milliseconds represents a minute
                                interval=1 * 250,  # in milliseconds
                                n_intervals=0
                            )
                        ]),
                    ]),
                    dcc.Tab(label="Simulation summary", value="summary_tab", children=[
                        html.Div([
                            dcc.Graph(
                                id='services-graph',
                                figure=charts.build_static_charts(total_time_descargas-service_processors_descargas, service_processors_descargas, total_time_cargas-service_processors_cargas
                                                                  , service_processors_cargas, total_time_duo, service_processors_duo, shifts, total_time_total - service_processors_total, service_processors_total)
                            ),
                            dcc.Graph(
                                id='entries-graph',
                                figure=charts.build_static_entries(entries_carregues, entries_descarregues, entries_duo, shifts, entries_total, max_queue_total, max_par_total)
                            ),
                            dcc.Graph(
                                id='queue-graph',
                                figure=charts.build_static_queue(max_queue_carregues, max_queue_descarregues,
                                                                 max_queue_duo, shifts)
                            ),
                            dcc.Graph(
                                id='parking-graph',
                                figure=charts.build_static_parquink(max_par_carregues, max_par_descarregues,
                                                                    max_par_duo, shifts)
                            )
                        ]),
                    ]),
                ],
                value="real_time_tab",
            )

        ],
            className="row tabs_div"
        ),

        html.Link(href="https://use.fontawesome.com/releases/v5.2.0/css/all.css", rel="stylesheet"),
        html.Link(
            href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",
            rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Dosis", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Open+Sans", rel="stylesheet"),
        html.Link(href="https://fonts.googleapis.com/css?family=Ubuntu", rel="stylesheet"),
        html.Link(
            href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css",
            rel="stylesheet")
    ]),
    className="row",
    style={"margin": "0%"},
)


@app.callback([Output('time-graph', 'figure'),
               Output('live-update-graph', 'figure'),
               Output('pie-graph', 'figure')],
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    global mainTime, df, entries, entriesTime, buffer_slots_busy, queue_slots_busy, buffer_max_size, queue_max_size, processors_max_number, processors_free, old_event_time, totalEntities, charts
    global timeline_cargas, timeline_descargas, timeline_duo, shifts

    mainTime += 60

    entries.append(0)
    totalEntities.append(totalEntities[-1])
    entriesTime.append(mainTime)
    entriesTimeNames.append(parse_time(mainTime))
    # print(parse_time(mainTime))

    correct = True
    size = len(df.index)
    count = 0
    while correct and (count < size):
        event = df.iloc[count]
        event_time = event['Current_Time']
        if event_time > mainTime:
            correct = False
        else:
            if event['Event_Name'] == 'NEXT_ARRIVAL':
                entries[-1] += 1
                queue_slots_busy = event['Queue_Length']
                processors_free = event['Number_Idle_Processors']
                buffer_slots_busy = event['Buffer_Length']
                totalEntities[-1] = event['Entities_System']
            count += 1
    df = df.iloc[count:]

    traces = []
    traces.append(go.Scatter(
        x=list(entriesTime),
        y=list(entries),
        name='Entrades',
        mode='lines+markers',
        type='scatter'
    ))
    traces.append(go.Scatter(
        x=list(entriesTime),
        y=list(totalEntities),
        name='Total entitats',
        mode='lines+markers',
        type='scatter'
    ))

    layout = go.Layout(
        title="Entrades de camions i número d'entitas dintre del port",
        xaxis={'type': 'log', 'title': 'Temps', 'ticktext': list(entriesTimeNames), 'tickvals': list(entriesTime)},
        yaxis={'title': 'Camions'},  # , 'range': [-10, 20]},
        # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
        legend={'x': 0, 'y': 1},
        hovermode='closest'
    )

    fig1 = {
        'data': traces,
        'layout': layout
    }

    fig2 = charts.build_queue_pies(buffer_slots_busy, queue_slots_busy, processors_free, buffer_max_size,
                                   queue_max_size, processors_max_number)
    fig3 = charts.build_timeline(mainTime, timeline_cargas, timeline_descargas, timeline_duo, shifts)

    return fig3, fig2, fig1


if __name__ == '__main__':
    app.run_server(debug=True)
