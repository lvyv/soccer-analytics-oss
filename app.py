import dash
from dash import dcc
from event_plotter import plot_events
from dash.dependencies import Input, Output, State
from team_radar import team_radar_builder
from dash import html
import glob
import dash_bootstrap_components as dbc
from fig_generator import fig_from_json
from initial_figures import (
    initial_figure_radar,
    initial_figure_simulator,
    initial_figure_events,
)
import dash_daq as daq

REDTROOP = "红方"
BLUETROOP = "蓝方"
# Create list of event csv files available to select from via a pulldown menu
event_file_list = glob.glob("data/*.csv")
event_files = [w.replace("data\\", "") for w in event_file_list]
event_files = [s for s in event_files if "统计" in s]

# Create list of tracking json files available to select from via a pulldown menu
tracking_file_list = glob.glob("data/*.json")
tracking_files = [w.replace("data\\", "") for w in tracking_file_list]
tracking_files = [s for s in tracking_files if "json" in s]

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}, ],
)
app.title = '复盘分析'
server = app.server

# Configure controls using Dash Design Kit
static_graph_controls = [
    dbc.FormGroup(
        [
            dbc.Label("演训数据文件:"),
            dbc.Select(
                id="event-file",
                options=[{"label": i, "value": i} for i in event_files],
                value=None,
                placeholder="选择演训数据文件",
            ),
        ]
    ),
    dbc.FormGroup(
        [
            dbc.Label("演训队伍:"),
            dbc.Select(
                id="team-dropdown",
                options=[{"label": i, "value": i} for i in [REDTROOP, BLUETROOP]],
                value=REDTROOP,
                placeholder="选择演训队伍",
            ),
        ]
    ),
]

simulator_controls = [
    dbc.FormGroup(
        [
            dbc.Label("演训日志数据:"),
            dbc.Select(
                id="tracking-file",
                options=[{"label": i, "value": i} for i in tracking_files],
                value=None,
                placeholder="选择需要复盘的演训数据文件",
            ),
        ]
    ),
    dbc.Card(
        daq.Knob(       # noqa
            id="speed-knob",
            label="复盘速度",
            value=2.5,
            max=5,
            color={"default": "#3598DC"},
            size=100,
        )
    ),
    dbc.Button("提交", className="mr-2", id="submit-button", color="info"),
]

# Configure main app layout
app.layout = dbc.Container(
    fluid=True,
    children=[
        html.Header([html.H3("复盘分析工具")]),
        dbc.Card(
            dbc.Row([dbc.Col(c) for c in static_graph_controls], form=True), body=True
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        children=[
                            dcc.Loading(
                                id="loading-icon1",
                                children=[
                                    dcc.Graph(
                                        id="radar-graph",
                                        figure=initial_figure_radar(),
                                        config={
                                            "modeBarButtonsToRemove": [
                                                "toggleSpikelines",
                                                "pan2d",
                                                "autoScale2d",
                                                "resetScale2d",
                                            ]
                                        },
                                    )
                                ],
                                type="default",
                            )
                        ]
                    ),
                ),
                dbc.Col(
                    dbc.Card(
                        children=[
                            dcc.Loading(
                                id="loading-icon2",
                                children=[
                                    dcc.Graph(
                                        id="events-shots",
                                        figure=initial_figure_events(),
                                        config={
                                            "modeBarButtonsToAdd": [
                                                "drawline",
                                                "drawopenpath",
                                                "drawcircle",
                                                "drawrect",
                                                "eraseshape",
                                            ],
                                            "modeBarButtonsToRemove": [
                                                "toggleSpikelines",
                                                "pan2d",
                                                "autoScale2d",
                                                "resetScale2d",
                                            ],
                                        },
                                    )
                                ],
                                type="default",
                            )
                        ]
                    ),
                ),
            ],
            form=True,
            no_gutters=False,
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        children=[
                            dcc.Loading(
                                id="loading-icon3",
                                children=[
                                    dcc.Graph(
                                        id="events-assists",
                                        figure=initial_figure_events(),
                                        config={
                                            "modeBarButtonsToAdd": [
                                                "drawline",
                                                "drawopenpath",
                                                "drawcircle",
                                                "drawrect",
                                                "eraseshape",
                                            ],
                                            "modeBarButtonsToRemove": [
                                                "toggleSpikelines",
                                                "pan2d",
                                                "autoScale2d",
                                                "resetScale2d",
                                            ],
                                        },
                                    )
                                ],
                                type="default",
                            )
                        ]
                    ),
                ),
                dbc.Col(
                    dbc.Card(
                        children=[
                            dcc.Loading(
                                id="loading-icon4",
                                children=[
                                    dcc.Graph(
                                        id="events-progressive-passes",
                                        figure=initial_figure_events(),
                                        config={
                                            "modeBarButtonsToAdd": [
                                                "drawline",
                                                "drawopenpath",
                                                "drawcircle",
                                                "drawrect",
                                                "eraseshape",
                                            ],
                                            "modeBarButtonsToRemove": [
                                                "toggleSpikelines",
                                                "pan2d",
                                                "autoScale2d",
                                                "resetScale2d",
                                            ],
                                        },
                                    )
                                ],
                                type="default",
                            )
                        ]
                    ),
                ),
            ],
            form=True,
            no_gutters=False,
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        children=[
                            dcc.Loading(
                                id="loading-icon5",
                                children=[
                                    dcc.Graph(
                                        id="events-crosses",
                                        figure=initial_figure_events(),
                                        config={
                                            "modeBarButtonsToAdd": [
                                                "drawline",
                                                "drawopenpath",
                                                "drawcircle",
                                                "drawrect",
                                                "eraseshape",
                                            ],
                                            "modeBarButtonsToRemove": [
                                                "toggleSpikelines"
                                            ],
                                        },
                                    )
                                ],
                                type="default",
                            )
                        ]
                    ),
                ),
                dbc.Col(
                    dbc.Card(
                        children=[
                            dcc.Loading(
                                id="loading-icon6",
                                children=[
                                    dcc.Graph(
                                        id="events-set-plays",
                                        figure=initial_figure_events(),
                                        config={
                                            "modeBarButtonsToAdd": [
                                                "drawline",
                                                "drawopenpath",
                                                "drawcircle",
                                                "drawrect",
                                                "eraseshape",
                                            ],
                                            "modeBarButtonsToRemove": [
                                                "toggleSpikelines",
                                                "pan2d",
                                                "autoScale2d",
                                                "resetScale2d",
                                            ],
                                        },
                                    )
                                ],
                                type="default",
                            )
                        ]
                    ),
                ),
            ],
            form=True,
            no_gutters=False,
        ),
        html.Br(),
        dbc.Row(
            [
                dbc.Card(simulator_controls),
                dbc.Col(
                    dbc.Card(
                        children=[
                            dcc.Loading(
                                id="loading-icon7",
                                children=[
                                    dcc.Graph(
                                        id="game-simulation",
                                        animate=True,
                                        figure=initial_figure_simulator(),
                                        config={
                                            "modeBarButtonsToAdd": [
                                                "drawline",
                                                "drawopenpath",
                                                "drawcircle",
                                                "drawrect",
                                                "eraseshape",
                                            ],
                                            "modeBarButtonsToRemove": [
                                                "toggleSpikelines",
                                                "pan2d",
                                                "autoScale2d",
                                                "resetScale2d",
                                            ],
                                        },
                                    )
                                ],
                                type="default",
                            )
                        ]
                    ),
                ),
            ],
            form=True,
            no_gutters=False,
        ),
    ],
)


# Callback for events data
@app.callback(
    [
        Output("events-shots", "figure"),
        Output("events-assists", "figure"),
        Output("events-progressive-passes", "figure"),
        Output("events-crosses", "figure"),
        Output("events-set-plays", "figure"),
    ],
    [Input("event-file", "value"), Input("team-dropdown", "value")],
    prevent_initial_call=True,
)
def event_graph(event_file, team):
    if team is not None and event_file is not None:
        fig_shots = plot_events("Shots", event_file, team, REDTROOP)
        fig_assists = plot_events("Assists to Shots", event_file, team, REDTROOP)
        fig_crosses = plot_events("Crosses", event_file, team, REDTROOP)
        fig_set_plays = plot_events("Set Plays", event_file, team, REDTROOP)
        fig_progressive_passes = plot_events(
            "Progressive Passes", event_file, team, REDTROOP
        )
        for x in [
            fig_shots,
            fig_assists,
            fig_crosses,
            fig_set_plays,
            fig_progressive_passes,
        ]:
            # Change modebar drawing item colour so that it stands out (vs. grey)
            x.update_layout(newshape=dict(line_color="#009BFF"))
        return (
            fig_shots,
            fig_assists,
            fig_crosses,
            fig_set_plays,
            fig_progressive_passes,
        )

    else:
        fig = initial_figure_events()
        return fig, fig, fig, fig, fig


# Callback for KPI Radar
@app.callback(
    Output("radar-graph", "figure"),
    [Input("event-file", "value"), Input("team-dropdown", "value")],
    prevent_initial_call=True,
)
def radar_graph(radar_file, team):
    if team is not None:
        fig = team_radar_builder(radar_file, team)
        return fig
    else:
        fig = initial_figure_radar()
        fig.update_layout(margin=dict(l=80, r=80, b=30, t=55))
        # Disable zoom. It just distorts and is not fine-tunable
        fig.layout.xaxis.fixedrange = True
        fig.layout.yaxis.fixedrange = True
        return fig


# Callback for animated game simulation graph
@app.callback(
    Output("game-simulation", "figure"),
    Input("submit-button", "n_clicks"),
    State("speed-knob", "value"),
    State("tracking-file", "value"),
    prevent_initial_call=True,
)
def game_simulation(n_clicks, speed, filename):
    print(n_clicks)
    speed_adjusted = speed * 100
    game_speed = 600 - speed_adjusted
    fig = fig_from_json("data/" + filename)     # noqa
    fig.update_layout(margin=dict(l=0, r=20, b=0, t=0))
    fig.update_layout(newshape=dict(line_color="#009BFF"))
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = game_speed
    fig.update_yaxes(scaleanchor="x", scaleratio=0.70)
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                y=-0.10,
                x=-0.08,
                xanchor="left",
                yanchor="bottom",
            )
        ]
    )
    fig.update_layout(autosize=True)
    fig.update_layout(modebar=dict(bgcolor="rgba(0, 0, 0, 0)", orientation="v"))
    # Disable zoom. It just distorts and is not fine-tunable
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True
    fig.update_layout(legend=dict(font=dict(family="Arial", size=10, color="grey")))
    # Sets background to be transparent
    fig.update_layout(
        template="plotly_dark",
        xaxis=dict(showgrid=False, showticklabels=False),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
    )
    fig["layout"]["template"]["data"]["scatter"][0]["marker"]["line"]["color"] = "white"
    fig["layout"]["template"]["data"]["scatter"][0]["marker"]["opacity"] = 0.9
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
