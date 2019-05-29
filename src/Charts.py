
class Charts:
    _instance = None

    def build_static_charts(self, idle_1, service_1, idle_2, service_2, idle_3, service_3):
        figure = {
            'data': [
                {
                    "values": [idle_1, service_1],
                    "labels": [
                        "Idle Processors",
                        "Service Processors"
                    ],
                    'marker': {'colors': ['rgb(255, 140, 0)',
                                          'rgb(65, 105, 225)']},
                    "domain": {"column": 0},
                    "hoverinfo": "label+value+name",
                    "hole": .4,
                    "type": "pie",
                    "title": "Etapa1",
                    'textinfo': 'label+text+percent',
                    'direction': 'clockwise',
                    'sort': False
                },
                {
                    "values": [idle_2, service_2],
                    "labels": [
                        "Idle Processors",
                        "Service Processors"
                    ],
                    'marker': {'colors': ['rgb(255, 140, 0)',
                                          'rgb(65, 105, 225)']},
                    "textposition": "inside",
                    "domain": {"column": 1},
                    "title": "Etapa2",
                    "hoverinfo": "label+value+name",
                    "hole": .4,
                    "type": "pie",
                    'textinfo': 'label+text+percent',
                    'direction': 'clockwise',
                    'sort': False
                },
                {
                    "values": [idle_3, service_3],
                    "labels": [
                        "Idle Processors",
                        "Service Processors"
                    ],
                    'marker': {'colors': ['rgb(255, 140, 0)',
                                          'rgb(65, 105, 225)']},
                    "textposition": "inside",
                    "domain": {"column": 2},
                    "title": "Etapa3",
                    "hoverinfo": "label+value+name",
                    "hole": .4,
                    "type": "pie",
                    'textinfo': 'label+text+percent',
                    'direction': 'clockwise',
                    'sort': False
                }
            ],
            'layout': {
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
        return figure

    def build_timeline(self, time, timeline_cargas, timeline_descargas, timeline_duo):
        hour = time/3600
        figure = {
            "data": [
                {
                    "name": "moment actual",
                    "mode": 'markers',
                    "showlegend": False,
                    "x": [hour],
                    "y": [0],
                    'marker': dict(
                        color='rgb(238, 32, 77)',
                        symbol=20,
                        size=20,
                        line=dict(
                            color='rgb(0, 0, 0)',
                            width=0.5
                        )
                    )
                },
                {
                    "type": "scatter",
                    "uid": "1bec64",
                    "line": {
                        "color": "rgb(51, 153, 102)",
                        "shape": "spline",
                        "width": 4
                    },
                    "mode": "lines",
                    "name": "Càrregues",
                    "x": timeline_cargas,
                    "y": [0] * len(timeline_cargas),
                    "error_y": {
                        "visible": False
                    }
                },
                {
                    "type": "scatter",
                    "uid": "1bec64",
                    "line": {
                        "color": "rgb(255, 153, 51)",
                        "shape": "spline",
                        "width": 4
                    },
                    "mode": "lines",
                    "name": "Descàrregues",
                    "x": timeline_descargas,
                    "y": [0] * len(timeline_descargas),
                    "error_y": {
                        "visible": False
                    }
                },
                {
                    "type": "scatter",
                    "uid": "1bec64",
                    "line": {
                        "color": "rgb(51, 153, 255)",
                        "shape": "spline",
                        "width": 4
                    },
                    "mode": "lines",
                    "name": "Càrregues+Descàrregues",
                    "x": timeline_duo,
                    "y": [0] * len(timeline_duo),
                    "error_y": {
                        "visible": False
                    }
                }
            ],
            'layout': {
                'title': 'Les diferents etapes de la simulació',
                'xaxis': {'title': '', 'showgrid': False, 'ticktext': list(range(6, 21)),
                          'tickvals': list(range(6, 21)),
                          'ticklen': 10, 'tickwidth': 2, 'tickcolor': '#000', 'anchor': 'free', 'overlaying': 'y',
                          'position': 0.5},
                'yaxis': {'title': '', 'showgrid': False, 'ticktext': [], 'tickvals': []},
                'height': 250,
            }
        }
        return figure

    def build_queue_pies(self, buffer_slots_busy, queue_slots_busy, processors_free, buffer_max_size, queue_max_size, processors_max_number):
        figure = {
            "data": [
                {
                    "values": [buffer_slots_busy, buffer_max_size - buffer_slots_busy],
                    "labels": [
                        "Busy slots",
                        "Free Slots"
                    ],
                    'marker': {'colors': ['rgb(255, 140, 0)',
                                          'rgb(65, 105, 225)']},
                    "domain": {"column": 0},
                    "hoverinfo": "label+value+name",
                    "hole": .4,
                    "type": "pie",
                    "title": "Cua",
                    'textinfo': 'label+text+value+percent',
                    'direction': 'clockwise',
                    'sort': False
                },
                {
                    "values": [queue_slots_busy, queue_max_size - queue_slots_busy],
                    "labels": [
                        "Busy slots",
                        "Free Slots"
                    ],
                    'marker': {'colors': ['rgb(255, 140, 0)',
                                          'rgb(65, 105, 225)']},
                    "textposition": "inside",
                    "domain": {"column": 1},
                    "title": "Pàrquink",
                    "hoverinfo": "label+value+name",
                    "hole": .4,
                    "type": "pie",
                    'textinfo': 'label+text+value+percent',
                    'direction': 'clockwise',
                    'sort': False
                },
                {
                    "values": [processors_max_number - processors_free, processors_free],
                    "labels": [
                        "Service-Processors",
                        "Idle-Processors"
                    ],
                    'marker': {'colors': ['rgb(255, 140, 0)',
                                          'rgb(65, 105, 225)']},
                    "textposition": "inside",
                    "domain": {"column": 2},
                    "title": "Processors",
                    "hoverinfo": "label+value+name",
                    "hole": .4,
                    "type": "pie",
                    'textinfo': 'label+text+value+percent',
                    'direction': 'clockwise',
                    'sort': False
                }
            ],
            "layout": {
                "title": "Número de camions a les diferents etapes del port",
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
        return figure



def Parameters():
    if Charts._instance is None:
        Charts._instance = Charts()
    return Charts._instance