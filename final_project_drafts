# -*- coding: utf-8 -*-
"""
Created on Thu May  4 09:49:00 2023

@author: egarciagonz
"""

import serial
import re
import time
import pandas as pd
import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from collections import deque
# import dash
# from dash.dependencies import Output, Input
# import dash_core_components as dcc
# import dash_html_components as html
# import ploty
# import random
# import ploty.graph_objs as go
# from collections import deque

SERIAL_SPEED = 9600
COM_PORT = 'COM3'
ser = serial.Serial()
ser.port = COM_PORT
ser.baudrate = SERIAL_SPEED

db =  pd.read_excel('PlantCare_DBASE.xlsx' )

X =deque(maxlen=20)
X.append(1)
Y =deque(maxlen=20)
Y.append(1)

X2 =deque(maxlen=20)
X2.append(1)
Y2 =deque(maxlen=20)
Y2.append(1)

temperature=[]
humidity=[]

def extract_data(ser):
    while(True):
        message= ser.readline()
        print (message)
        data_string = message.decode("utf-8")
        temp = re.findall('<temp=([\d]+[.,\d]+),', data_string)
        print(temp)
        humid = re.findall(',humid=([\d]+)>', data_string)
        print(humid)
        
        if temp != []:
            global temperature
            temperature = [float(s) for s in temp]
        if humid != []:
            global humidity
            humidity = [float(s) for s in humid]
        return temperature, humidity
    
try:
    ser.open()
    if ser.isOpen():
        print("Port " + ser.port + " opened successfully")
except Exception as e:
    print(e)


app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout

tab1 = dbc.Card(
    dbc.CardBody([
        dbc.Row([  
            html.Br(),
            html.H2('What plant are we taking care of today?'),
        ]),
        
       dbc.Row([     
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
                    id='switch',
                    on=False,
                    label="OFF / ON",
                    labelPosition="top"
                ),
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
    ]),
    className="mt-1",
)

tab2 = dbc.Card(
    dbc.CardBody([
        dbc.Row([
            dcc.Graph(id="data-graph1"),
            dcc.Interval(id="interval-component1", interval=2000, n_intervals=0)
        ]),
        
        html.Br(),
        html.Br(),
        
        dbc.Row([
            dcc.Graph(id="data-graph2"),
            dcc.Interval(id="interval-component2", interval=2000, n_intervals=0)])
        ]),
    ),

app.layout = dbc.Container([

    dbc.Row([ #index kind of thing/homepage
        dbc.Col([
            html.H1('Welcome to your Smart Irrigation System Homepage'),
            html.Br(),
            html.Br(),
            html.H3('Choose what type of system you would like to work with today: Automatic or Manual'),
        ])
    ]),
    
    html.Br(),
    html.Br(),

        
    dbc.Row([ #indicate type of plant and if it's indoor/outdoor
       dbc.Col([
          dcc.Tabs([
              dcc.Tab(tab1, label='Automatic Plant Care System'), 
              dcc.Tab(tab2, label='Manual Plant Care System - Data'),    
          ]),
      ]),
    ]),
    
    #html.Div(id='switch-output')
], className="mt-4")



# Callbacks
@app.callback(dash.dependencies.Output(component_id='data-graph1', component_property='figure'), 
              dash.dependencies.Output(component_id='data-graph2', component_property='figure'),
              Input('planttype', 'value'), dash.dependencies.Input('interval-component1', 'n_intervals'), 
              dash.dependencies.Input('interval-component2', 'n_intervals'),
              [State('switch', 'on'), State('environment','on')])

def show_values(planttype, n1, n2, switch, environment) :
    
    extract_data(ser)
    
    if temperature != []:
        X.append(X[-1]+1)
    for i in temperature:
        Y.append(i)
    
    if humidity != []:
        X2.append(X2[-1]+1)
    for i in humidity:
        Y2.append(i)
        
    print('lista x')
    print(*list(X))
    print('lista y')
    print(*list(Y))
    
    
    data_out1 = go.Figure(go.Scatter(x = list(X), y=list(Y)))
    data_out1.update_layout(
        title= "Temperature through time",
        xaxis_title="Time (s)",
        yaxis_title="Temperature (ºC)")
    
    print('lista x2')
    print(*list(X2))
    print('lista y2')
    print(*list(Y2))
    
    data_out2 = go.Figure(go.Scatter( x = list(X2), y=list(Y2)))
    data_out2.update_layout(
        title= "Humidity through time",
        xaxis_title="Time (s)",
        yaxis_title="Humidity (%)"),
    
    
    
    if switch:    
        
        tipo_planta=planttype

        myplant_info = db[db['Name'] == tipo_planta]
        print(myplant_info)

        if temperature[-1] >= myplant_info['Temperature'].iloc[0]:
          commandt = 'warm\n'
          ser.write(commandt.encode("utf-8"))
     
        else:
          commandt = 'cold\n'
          ser.write(commandt.encode("utf-8"))
     
        if humidity[-1] >= myplant_info['Humidity'].iloc[0]:
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
        print(commandsun)    
        print(commandt)
        print(commandh)
        time.sleep(2)

        
    else:
        
        commandt = 'warm\n'
        ser.write(commandt.encode("utf-8"))
        commandh = 'humid\n'
        ser.write(commandh.encode("utf-8"))
        commandsun = 'outdoor\n'
        ser.write(commandsun.encode("utf-8"))
        
        #return {}
    return {'data':[data_out1], 'Layout':go.Layout(xaxis_title='Time Step (2s)',yaxis_title='Temperature (ºC)',)}, {'data':[data_out2], 'Layout':go.Layout(xaxis_title='Time Step (2s)',yaxis_title='Humidity (%)',)}

#Execution
app.run_server(port=8061)

ser.close()
