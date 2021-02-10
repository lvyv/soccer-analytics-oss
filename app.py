import dash
import dash_design_kit as ddk
import dash_core_components as dcc
from event_plotter import plotEvents
from dash.dependencies import Input, Output, State
from team_radar import team_radar_builder
import dash_html_components as html
import glob
#import os
from fig_generator import fig_from_json
#from ids import IDS
#import pages
#import traceback
from initial_figures import initial_figure_radar, initial_figure_simulator, initial_figure_events

# Theme export from Theme Builder to tailor the app's appearance
theme = {
    "accent":"#1f78b4",
    "accent_positive":"#017500",
    "accent_negative":"#C20000",
    "background_content":"#282828",
    "background_page":"rgb(25,25,25)",
    "body_text":"#aaaaaa",
    "border":"#e2e2e2",
    "border_style":{
        "name":"underlined",
        "borderWidth":"0px 0px 1px 0px",
        "borderStyle":"solid",
        "borderRadius":0
    },
    "button_border":{
        "width":"1px",
        "color":"#1f78b4",
        "radius":"30px"
    },
    "button_capitalization":"uppercase",
    "button_text":"#1f78b4",
    "button_background_color":"#282828",
    "control_border":{
        "width":"0px",
        "color":"#e2e2e2",
        "radius":"0px"
    },
    "control_background_color":"rgb(25,25,25)",
    "control_text":"#606060",
    "card_margin":"7px",
    "card_padding":"5px",
    "card_border":{
        "width":"0px",
        "style":"solid",
        "color":"#e2e2e2",
        "radius":"0px"
    },
    "card_background_color":"#282828",
    "card_box_shadow":"0 0 0 #232323",
    "card_outline":{
        "width":"0px",
        "style":"solid",
        "color":"#e2e2e2"
    },
    "card_header_margin":"0px",
    "card_header_padding":"5px",
    "card_header_border":{
        "width":"0px",
        "style":"solid",
        "color":"#e2e2e2",
        "radius":"0px"
    },
    "card_header_background_color":"#282828",
    "card_header_box_shadow":"0px 0px 0px rgba(0,0,0,0)",
    "breakpoint_font":"1200px",
    "breakpoint_stack_blocks":"700px",
    "colorway":[
        "#00bfff",
        "#66c2a5",
        "#fc8d62",
        "#e78ac3",
        "#a6d854",
        "#ffd92f",
        "#e5c494",
        "#b3b3b3"
    ],
    "colorscale":[
        "#1f78b4",
        "#4786bc",
        "#6394c5",
        "#7ba3cd",
        "#92b1d5",
        "#a9c0de",
        "#bed0e6",
        "#d4dfee",
        "#eaeff7",
        "#ffffff"
    ],
    "dbc_primary":"#1f78b4",
    "dbc_secondary":"#ffffff",
    "dbc_info":"#009AC7",
    "dbc_gray":"#adb5bd",
    "dbc_success":"#017500",
    "dbc_warning":"#F9F871",
    "dbc_danger":"#C20000",
    "font_family":"Open Sans",
    "font_family_header":"Open Sans",
    "font_family_headings":"Open Sans",
    "font_size":"17px",
    "font_size_smaller_screen":"15px",
    "font_size_header":"24px",
    "title_capitalization":"uppercase",
    "header_content_alignment":"spread",
    "header_margin":"0px 0px 15px 0px",
    "header_padding":"0px",
    "header_border":{
        "width":"0px",
        "style":"solid",
        "color":"#e2e2e2",
        "radius":"0px"
    },
    "header_background_color":"#282828",
    "header_box_shadow":"none",
    "header_text":"#aaaaaa",
    "heading_text":"#aaaaaa",
    "text":"#aaaaaa",
    "report_background_content":"#FAFBFC",
    "report_background_page":"white",
    "report_text":"black",
    "report_font_family":"Computer Modern",
    "report_font_size":"12px"
}

# Create list of event csv files available to select from via a pulldown menu
event_file_list = (glob.glob("data/*.csv"))
event_files = [w.replace('data/', '') for w in event_file_list]
event_files = [s for s in event_files if "Event" in s]

# Create list of tracking json files available to select from via a pulldown menu
tracking_file_list = (glob.glob("data/*.json"))
tracking_files = [w.replace('data/', '') for w in tracking_file_list]
tracking_files = [s for s in tracking_files if "json" in s]

app = dash.Dash(__name__)
server = app.server
#os.environ["SNAPSHOT_DATABASE_URL"] = os.environ.get("DATABASE_URL", "postgres://username:password@127.0.0.1:5432") if os.name == 'nt' else os.environ.get("DATABASE_URL", "sqlite:///snapshot-dev.db")
#snap = dash_snapshots.DashSnapshots(app)
#celery_instance = snap.celery_instance

# Configure controls using Dash Design Kit
static_graph_controls = [
    ddk.ControlItem(
        dcc.Dropdown(
            id= 'event-file',
            options=[
                {'label': i, 'value': i}
                for i in event_files
            ],
            multi=False,
            value=None
        ),
        label='Events File:',
    ),
    ddk.ControlItem(
        dcc.Dropdown(
            id='team-dropdown',
            multi=False,
            options=[{'label': i, 'value': i} for i in ['Home', 'Away']],
            value='Home'
        ),
        label='Team:',
    ),

    #dcc.Location(id=IDS['LOCATION']),
    #html.Div(id='content')

]
simulator_controls = [
    ddk.ControlItem(
        dcc.Dropdown(
            id='tracking-file',
            options=[
                {'label': i, 'value': i}
                for i in tracking_files
            ],
            multi=False,
            value=None
        ),
        label='Tracking File:',
    ),

    ddk.ControlItem(
        dcc.Slider(
            id='speed-slider',
            min=100,
            max=500,
            step=1,
            value=300,
            marks={
                100: '1',
                200: '2',
                300: '3',
                400: '4',
                500: '5'
            },
            included=True
        ),
        label='Playback Speed:',
    ),

    html.Button('Submit', id='submit-button')
]

# Configure main app layout
app.layout = ddk.App(theme=theme, children=[
    ddk.Header([
        ddk.Logo(src=app.get_asset_url('logo.png')),
        ddk.Title('Match Analysis Tool'),
        ddk.Menu([

            html.Div(id='button-container', children=html.Span([
                html.Span(id='take-snapshot-status'),
                html.Button('Take Snapshot', id='take-snapshot'),
            ])),

            dcc.Link(
                href=app.get_relative_path('/'),
                children='Home'
            ),

            dcc.Link(
                href=app.get_relative_path('/archive'),
                children='Archive'
            )
        ])
    ]),

    ddk.Row([
        ddk.ControlCard(static_graph_controls,  orientation='horizontal'),
    ]),
    ddk.Row([
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon1",
                        children=[ddk.Graph(id='radar-graph', figure=initial_figure_radar(),
                        config={'modeBarButtonsToRemove': ['toggleSpikelines', 'pan2d', 'autoScale2d','resetScale2d']})], type="default",
                        )
            ]
        ),
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon2",
                        children=[ddk.Graph(id='events-shots', figure=initial_figure_events(),
                        config = {'modeBarButtonsToAdd':['drawline',
                                        'drawopenpath',
                                        'drawcircle',
                                        'drawrect',
                                        'eraseshape'
                                       ], 'modeBarButtonsToRemove':['toggleSpikelines', 'pan2d', 'autoScale2d', 'resetScale2d']})], type = "default",
                        )
            ]
        ),
    ]),

    ddk.Row([
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon3",
                        children=[ddk.Graph(id='events-assists', figure=initial_figure_events(),
                                            config={'modeBarButtonsToAdd':['drawline',
                                        'drawopenpath',
                                        'drawcircle',
                                        'drawrect',
                                        'eraseshape'
                                       ], 'modeBarButtonsToRemove':['toggleSpikelines', 'pan2d', 'autoScale2d', 'resetScale2d']})], type="default",
                        )
            ]
         ),
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon4",
                        children=[ddk.Graph(id='events-progressive-passes', figure=initial_figure_events(),
                                            config={'modeBarButtonsToAdd':['drawline',
                                        'drawopenpath',
                                        'drawcircle',
                                        'drawrect',
                                        'eraseshape'
                                       ], 'modeBarButtonsToRemove':['toggleSpikelines', 'pan2d', 'autoScale2d', 'resetScale2d']})], type="default",
                        )
            ]
        ),
    ]),

    ddk.Row([
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon5",
                        children=[ddk.Graph(id='events-crosses', figure=initial_figure_events(),
                                            config={'modeBarButtonsToAdd':['drawline',
                                        'drawopenpath',
                                        'drawcircle',
                                        'drawrect',
                                        'eraseshape'
                                       ], 'modeBarButtonsToRemove':['toggleSpikelines']})], type="default",
                        )
            ]
         ),
        ddk.Card(width=50, children=[
            dcc.Loading(id="loading-icon6",
                        children=[ddk.Graph(id='events-set-plays', figure=initial_figure_events(),
                                            config={'modeBarButtonsToAdd':['drawline',
                                        'drawopenpath',
                                        'drawcircle',
                                        'drawrect',
                                        'eraseshape'
                                       ], 'modeBarButtonsToRemove':['toggleSpikelines', 'pan2d', 'autoScale2d', 'resetScale2d']})], type="default",
                        )
            ]
        ),
    ]),

    ddk.Row([
        ddk.ControlCard(simulator_controls, width=25),
        ddk.Card(width=75, children=[
            dcc.Loading(id="loading-icon7",
                        children=[ddk.Graph(id='game-simulation', animate=True,  figure=initial_figure_simulator(),
                                            config={'modeBarButtonsToAdd':['drawline',
                                        'drawopenpath',
                                        'drawcircle',
                                        'drawrect',
                                        'eraseshape'
                                       ], 'modeBarButtonsToRemove':['toggleSpikelines', 'pan2d', 'autoScale2d', 'resetScale2d']})], type="default",
                                            )
        ]),
    ]),
])

# Callback for events data
@app.callback(
    [Output('events-shots', 'figure'),Output('events-assists', 'figure'),Output('events-progressive-passes', 'figure'),
     Output('events-crosses', 'figure'),Output('events-set-plays', 'figure')],
    [Input('event-file', 'value'),
     Input('team-dropdown', 'value')], prevent_initial_call=True)
def event_graph(event_file, team):
    if team is not None and event_file is not None:
        fig_shots = plotEvents('Shots', event_file, team, 'Home')
        fig_assists = plotEvents('Assists to Shots', event_file, team, 'Home')
        fig_crosses = plotEvents('Crosses', event_file, team, 'Home')
        fig_set_plays = plotEvents('Set Plays', event_file, team, 'Home')
        fig_progressive_passes = plotEvents('Progressive Passes Into Final 3rd', event_file, team, 'Home')
        for x in [fig_shots, fig_assists,fig_crosses, fig_set_plays, fig_progressive_passes]:
            # Change modebar drawing item colour so that it stands out (vs. grey)
            x.update_layout(newshape=dict(line_color='#009BFF'))
        return fig_shots, fig_assists, fig_crosses, fig_set_plays, fig_progressive_passes

    else:
        fig = initial_figure_events()
        return fig, fig, fig, fig, fig

# Callback for KPI Radar
@app.callback(
    Output('radar-graph', 'figure'),
    [Input('event-file', 'value'),
    Input('team-dropdown', 'value')],prevent_initial_call=True)
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
    Output('game-simulation', 'figure'),
    Input('submit-button','n_clicks'), State('speed-slider', 'value'), State('tracking-file', 'value'), prevent_initial_call=True)
def game_simulation_graph(n_clicks, speed, filename):
    game_speed = 600 - speed
    fig = fig_from_json('data/'+filename)
    fig.update_layout(margin=dict(l=0, r=20, b=0, t=0))
    fig.update_layout(
        newshape=dict(line_color='#009BFF'))
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = game_speed
    fig.update_yaxes(
                scaleanchor="x",
                scaleratio=.70)
    fig.update_layout(updatemenus=[dict(type='buttons',
                      showactive=False,
                      y=-0.10,
                      x=-0.08,
                      xanchor='left',
                      yanchor='bottom')
                            ])
    fig.update_layout(autosize=True)
    # Disable zoom. It just distorts and is not fine-tunable
    fig.layout.xaxis.fixedrange = True
    fig.layout.yaxis.fixedrange = True
    fig.update_layout(
    legend=dict(
        font=dict(
            family="Arial",
            size=10,
            color="grey"
            )
        )
    )
    return fig


'''# Snapshot callback
@app.callback(
    [Output('content', 'children'),
     Output('button-container', 'style')],
    [Input(IDS['LOCATION'], 'pathname')])
def display_content(pathname):
    button_style = {'hidden': {'width': 0, 'visibility': 'hidden'}, 'displayed': None}
    page_name = app.strip_relative_path(pathname)
    if not page_name:  # None or ''
        return [pages.home.layout(), button_style['displayed']]
    elif page_name == 'archive':
        return [pages.archive.layout(), button_style['hidden']]
    elif page_name.startswith("snapshot-"):
        return [pages.snapshot.layout(page_name), button_style['hidden']]
    elif page_name == 'dev':
        # Display a report with mock data for development purposes
        return [pages.snapshot.report(), button_style['hidden']]
    else:
        return ['404', button_style['hidden']]


@app.callback(
    Output('take-snapshot-status', 'children'),
    [Input('take-snapshot', 'n_clicks')],
    [State(IDS['GRAPH-1'], 'figure'),
     State(IDS['GRAPH-2'], 'figure'),
     State(IDS['GRAPH-3'], 'figure')],
    prevent_initial_call=True)
def save_snapshot(n_clicks, figure_1, figure_2, figure_3):
    try:
        # Submit task to save snapshot data and generate PDF in background
        snap.snapshot_save_async(
            save_snapshot_in_background,
            figure_1, figure_2, figure_3
        )
        return 'Saved!'
    except Exception as e:
        traceback.print_exc()
        return 'An error occurred saving this snapshot'


@snap.celery_instance.task
@snap.snapshot_async_wrapper(save_pdf=True)
def save_snapshot_in_background(figure_1, figure_2, figure_3):
    # This function is called in a separate task queue managed by celery
    # This function's parameters (temperature, pressure, humidity) are
    # provided by the callback above with `snap.snapshot_save_async`

    # Whatever is returned by this function will be saved to the database
    # with the `snapshot_id`. It needs to be JSON-serializable

    # In this case, we're just returning a pandas dataframe
    # This dataframe is loaded by `snapshot.layout` and transformed
    # into a set of `ddk.Report` & `ddk.Page` components.
    # This allows you to change your `ddk.Report` & `ddk.Page` reports
    # for older datasets.

    # You could also return a `ddk.Report` etc here if you want previously
    # saved reports to not change when you deploy new changes to your
    # `ddk.Report` layout code
    return {'figure-1': figure_1, 'figure-2': figure_2, 'figure-3': figure_3}'''


if __name__ == '__main__':
    app.run_server(debug=False)


