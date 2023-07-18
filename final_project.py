# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import serial
import re
import time
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from collections import deque

SERIAL_SPEED = 9600
COM_PORT = 'COM5'
ser = serial.Serial()
ser.port = COM_PORT
ser.baudrate = SERIAL_SPEED

db =  pd.read_excel('PlantCare_DBASE.xlsx' )

X =deque(maxlen=20)
X.append(1)
Y =deque(maxlen=20)
Y.append(1)

X1 =deque(maxlen=20)
X1.append(1)
Y1 =deque(maxlen=20)
Y1.append(1)

temperature=[]
humidity=[]
def extract_data(ser):
    while(True):
        message= ser.readline()
        data_string = message.decode("utf-8")
        temp = re.findall('<temp=([\d]+[.,\d]+),', data_string)
        humid = re.findall(',humid=([\d]+)>', data_string)
        if temp != []:
            global temperature
            temperature = [float(s) for s in temp]
        if humid != []:
            global humidity
            humidity = [float(s) for s in humid]
            print(humidity)
        return temperature, humidity
    
    
    
    
try:
    ser.open()
    if ser.isOpen():
        print("Port " + ser.port + " opened successfully")
except Exception as e:
    print(e)


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.MINTY])

# Layout

app.layout = dbc.Container([
  
    dbc.Row([ 
        dbc.Col([
            html.H1('Welcome to your Smart Irrigation System Homepage', 
                    className='text-center text-primary mb-4' ),
            html.Br(),
            html.Br(),
            html.H2('What are you planning to do today?', 
                    className='text-center text-muted mb-4'),

        ])
    ]),
    html.Br(),
    html.Br(),
    dbc.Tabs([
        dbc.Tab([
    dbc.Row([
        dbc.Col([
            html.H3('What plant are we taking care of today?'),
            html.Br(),
            dcc.Dropdown(
                id='planttype',
                options=[{'label': i, 'value': i} for i in db['Name']],
                value='Cactus',
            ),
        ]),

    dbc.Col([
        daq.BooleanSwitch(
            id='switch',
            on=False,
            label="OFF / ON",
            labelPosition="top"
        )
    ]),

        dbc.Col([
            daq.BooleanSwitch(
                id='environment',
                on=True,
                label="OUTDOOR / INDOOR",
                labelPosition="bottom"
            )
        ], width=2)
    ], justify="center", style={"margin-top": "5rem"}),
    
    ], label="Automatic plant care"),
        
    dbc.Tab([    
    
    dbc.Row([
        html.Div([
        dcc.Graph(id="data-graph1"),
        dcc.Interval(id="interval-component1", interval=2000, n_intervals=0)
        ])
        ]),
    dbc.Row([
        html.Div([
        dcc.Graph(id="data-graph2"),
        dcc.Interval(id="interval-component2", interval=2000, n_intervals=0)
        ])
        ]),
    ], label="Manual plant care")
    ]),
    html.Div(id='switch-output')
], className="mt-4")


# Callbacks
@app.callback(dash.dependencies.Output(component_id='data-graph1', 
                                       component_property='figure'),
              dash.dependencies.Output(component_id='data-graph2', 
                                       component_property='figure'),
              Input('planttype', 'value'), 
              dash.dependencies.Input('interval-component1', 'n_intervals'), 
              dash.dependencies.Input('interval-component2', 'n_intervals'),
              [State('switch', 'on'), State('environment','on')])
def show_values(planttype, n1,n2, switch, environment) :
    extract_data(ser)
    if temperature != []:
        X.append(X[-1]+1)
    for i in temperature:
        Y.append(i)

    data_out1 = go.Figure(data=go.Scatter( x = list(X), y=list(Y), 
                                          mode='lines', 
                                          line=dict(color = '#ff7851') ),  
                          layout=go.Layout(
                              title=go.layout.Title(
                                  text="<b>Temperature (ºC)</b>",
                                  font=dict(family='Montserrat',size=18, 
                                            color='#ff7851'))))
    
    if humidity != []:
        X1.append(X1[-1]+1)
    for i in humidity:
        Y1.append(i)
    
    data_out2 = go.Figure(data=go.Scatter( x = list(X1), y=list(Y1), 
                                          mode='lines', 
                                          line=dict(color = '#6cc3d5')), 
                          layout=go.Layout(title=go.layout.Title(
                              text="<b>Humidity (%)</b> ",
                              font=dict(family='Montserrat',size=18, 
                                        color='#6cc3d5'))))
    
    
    if switch:
        
        
        tipo_planta=planttype
        data=extract_data(ser)

        myplant_info = db[db['Name'] == tipo_planta]

        if data[0] >= myplant_info['Temperature'].iloc[0]:
          commandt = 'warm\n'
          ser.write(commandt.encode("utf-8"))
     
        else:
          commandt = 'cold\n'
          ser.write(commandt.encode("utf-8"))
     
        if data[1] >= myplant_info['Humidity'].iloc[0]:
          commandh = 'humid\n'
          ser.write(commandh.encode("utf-8"))
     
        else:
          commandh = 'dry\n'   
          ser.write(commandh.encode("utf-8"))
        if environment:
            commandsun = 'indoor\n'
            ser.write(commandsun.encode("utf-8"))
            
        else:
            commandsun = 'outdoor\n'
            ser.write(commandsun.encode("utf-8")) 
        time.sleep(2)      
    else:
        commandt = 'warm\n'
        ser.write(commandt.encode("utf-8"))
        commandh = 'humid\n'
        ser.write(commandh.encode("utf-8"))
        commandsun = 'outdoor\n'
        ser.write(commandsun.encode("utf-8"))
    return [data_out1, data_out2]

#Execution
app.run_server(port=8061)

ser.close()
