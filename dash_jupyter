import dash
from dash import html, dcc, dash_table
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_daq as daq
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go

###########

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout

app.layout = dbc.Container([
  
    dbc.Row([ #index kind of thing/homepage
        dbc.Col([
            html.H1('Welcome to your Smart Irrigation System Homepage'),
            html.Br(),
            html.Br(),
            html.H2('What are you planning to do today?'),

        ])
    ]),
  
    dbc.Row([ #indicate type of plant and if it's indoor/outdoor
        dbc.Col([
            
            dcc.Dropdown(
                id='planttype',
                options=[
                {'label': 'Cactus', 'value':'Cactus'},
                {'label': 'Rose', 'value':'Rose'},
                {'label': 'Daisy', 'value':'Daisy'},
                {'label': 'Tulip', 'value':'Tulip'},
                {'label': 'Sunflower', 'value':'Sunflower'},
                {'label': 'Hydrangea', 'value':'Hydrangea'},
                {'label': 'Succulent', 'value':'Succulent'},
                {'label': 'Orchid', 'value':'Orchid'},
                {'label': 'Mint', 'value':'Mint'},
                {'label': 'Rosemary', 'value':'Rosemary'},
                {'label': 'Basil', 'value':'Basil'},
                {'label': 'Thyme', 'value':'Thyme'},
                {'label': 'Tomato', 'value':'Tomato'},
                {'label': 'Strawberry', 'value':'Strawberry'},
                ],
                value='Cactus'
            ),

        ]),

    dbc.Col([
        daq.BooleanSwitch(
            on=True,
            label="ON / OFF",
            labelPosition="top"
        )
    ]),

        dbc.Col([
            daq.BooleanSwitch(
                id='environment',
                on=True,
                label="INDOOR / OUTDOOR",
                labelPosition="bottom"
            )
        ], width=2)
    ], justify="center", style={"margin-top": "5rem"}),
    
    dbc.Row([
        html.Div([
        dcc.Graph(id="data-graph"),
        dcc.Interval(id="interval-component", interval=2000, n_intervals=0)
        ])
        ]),
    
    html.Div(id='switch-output')
], className="mt-4")


# Callbacks
@app.callback(dash.dependencies.Output(component_id='data-graph', component_property='figure'),
              [Input('planttype', 'value'), Input('environment', 'value'), dash.dependencies.Input('interval-component', 'n_intervals')])
def show_values(planttype, environment, n):
    # set temperatura
    y = []
    trace = go.Scatter(y=y)
    fig = go.Figure(data=[trace])
    fig.update_xaxes(showticklabels=False)
    return fig

#Execution
app.run_server(port=8061)
