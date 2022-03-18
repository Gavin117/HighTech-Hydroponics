import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import datetime

grow_start = datetime.datetime(2021,5,1)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}




################################# Dashboard Layout ###########################################
##############################################################################################

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='HighTech Hydroponics',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'marginBottom' : "25px",
            'paddingTop' : "50px",
            'paddingBottom' : "70px",
            'paddingLeft' : "150px",
            'fontSize' : '62px'
        }
    ),
    
    
    html.Div(style = {'display':'flex', 'marginTop':'2rem','marginBottom':'4rem','paddingLeft':'150px', 'alignItems':'center'},
     children = [
            html.H4( id = 'schedule',
                    children='Schedule:', style={'color': '#fff','fontSize': '4.5rem'}
                ),
            html.H4( id = 'info',
                    children='(Day 0) Germination', style={'color': colors['text'], 'fontSize':'3.5rem', 'paddingLeft':'3rem'}
                )
            ]
    ),
    
    
###################################################################################################
    html.Div(style={
        'display':'flex',
        'justifyContent': 'space-between',
        'marginLeft':'150px',
        'marginRight': '150px'
    },children=[
            html.H4( id = 'temph4',
                    children='Test Temp', style={
                'textAlign': 'center',
                'color': colors['text'],
                'fontSize': '5.5rem',
                'width':'25%',
                'backgroundColor': '#FF0000',
                'borderRadius':'10px',
                'display':'inline-block'
            }),
            
            
            html.H4(id = 'phh4',
                    children='Test PH', style={
                'textAlign': 'center',
                'color': colors['text'],
                'fontSize': '5.5rem',
                'width':'25%',
                'backgroundColor': '#228B22',
                'borderRadius':'10px',
                'display':'inline-block'
            }),

            html.H4(id = 'co2h4',
                    children='Test C02', style={
                'textAlign': 'center',
                'color': colors['text'],
                'fontSize': '5.5rem',
                'width':'25%',
                'backgroundColor': '#0000FF',
                'borderRadius':'10px',
                'display':'inline-block'
            })
            ]
    ),
    
    dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
    ),
###################################################################################################

    html.H3(children='Enviornmental History', style={
        'textAlign': 'left',
        'color': colors['text'],
        'paddingLeft':'150px',
        'paddingTop':'70px'
    }),
    
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'temp', 'value': 'temp'},
            {'label': 'ph', 'value': 'ph'},
            {'label': 'co2', 'value': 'co2'}
        ],
        value="ph",
        style = dict(
            width = '40%',
            verticalAlign = "middle",
            paddingLeft = "150px"
            )
    ),


    dcc.Graph(
        id='graph-container',
        style={
        'paddingLeft':'100px',
        'paddingRight':'70px'})
])

###################################### CallBacks ##################################################
###################################################################################################

@app.callback(
    Output('graph-container', 'figure'),
    [Input('dropdown', 'value')])
def update_Graph(value):
    df = pd.read_csv(f'C:\\Users\\G_56\\Desktop\\projects\\hightech-hydroponics\\sensor_data\\{value}.csv').set_index('Date')
    fig = px.line(df, y=df[df.columns[0]])
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'])
    return fig


@app.callback(
    Output('temph4', 'children'),
    [Input('interval-component', 'n_intervals')])
def update_temp(n):
    with open('C:\\Users\\G_56\\Desktop\\projects\\hightech-hydroponics\\sensor_data\\temp.csv','r') as f:
        txt = f.readlines()[-1]
        f.close()
    result = txt.split(',')
    txt = result[1]
    degrees = u'\N{DEGREE SIGN}'
    return html.P(f'Temp: {txt}{degrees}C')

@app.callback(
    Output('phh4', 'children'),
    [Input('interval-component', 'n_intervals')])
def update_ph(n):
    with open('C:\\Users\\G_56\\Desktop\\projects\\hightech-hydroponics\\sensor_data\\ph.csv','r') as f:
        txt = f.readlines()[-1]
        f.close()
    result = txt.split(',')
    txt = result[1]
    return html.P(f'PH-Level:  {txt}')

@app.callback(
    Output('co2h4', 'children'),
    [Input('interval-component', 'n_intervals')])
def update_co2(n):
    with open('C:\\Users\\G_56\\Desktop\\projects\\hightech-hydroponics\\sensor_data\\co2.csv','r') as f:
        txt = f.readlines()[-1]
        f.close()
    result = txt.split(',')
    txt = result[1]
    return html.P(f'Co2: {txt} ppm')




if(__name__ == "__main__"):
    app.run_server(debug=True)
