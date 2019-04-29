import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
import geocoder
from datetime import datetime
import forecastio
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import argparse

def weather_on(loca):
    a = geocoder.location(location=loca)
    api_key = "c5dde0bafce3442350c75b743864339a"
    lat = a.latlng[0]
    lng = a.latlng[1]
    forecast = forecastio.load_forecast(api_key, lat, lng, time=datetime.now())
    byHour = forecast.hourly()
    return byHour

def weather_latest(loca):
    a = geocoder.location(location=loca)
    api_key = "c5dde0bafce3442350c75b743864339a"
    lat = a.latlng[0]
    lng = a.latlng[1]
    forecast = forecastio.load_forecast(api_key, lat, lng, time=datetime.now())
    this = forecast.currently().d
    return this

def get_sum_td(this):
    keys= []
    val=[]
    for k, v in this.items():
        keys.append(k.capitalize())
        val.append(v)
    return keys, val

def get_icon(byhour):
    return byhour.icon

def get_summary(byhour):
    return byhour.summary

def get_cur_temp(this):
    return this['temperature']

def get_cur_pro(this):
    return this['precipProbability']

def get_cur_h(this):
    return this['humidity']

def get_data_24h(byhour):
    temp = []
    date = []
    for hourlyData in byhour.data:
        temp.append(hourlyData.temperature)
        date.append(hourlyData.time)
    return temp, date

def get_data_24h_clo(byhour):
    clo = []
    date = []
    for hourlyData in byhour.data:
        clo.append(hourlyData.d['cloudCover'])
        date.append(hourlyData.time)
    return clo, date

def get_data_24h_pre(byhour):
    clo = []
    date = []
    for hourlyData in byhour.data:
        clo.append(hourlyData.d['precipProbability'])
        date.append(hourlyData.time)
    return clo, date

def get_data_24h_in(byhour):
    clo = []
    date = []
    for hourlyData in byhour.data:
        clo.append(hourlyData.d['precipIntensity'])
        date.append(hourlyData.time)
    return clo, date

app = dash.Dash()
app.title = 'Weather || Astrool'
image_filename = 'obj.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
static_image_route = 'Icons/'

app.layout = html.Div([
    html.Link(rel="shortcut icon", href="favicon.ico"),
    html.Img(
                src='data:image/png;base64,{}'.format(encoded_image.decode()),
                style={
                    'width': '20%',
                    'margin-left': '40%',
                    'margin-right': 'auto'
                },
             ),
    html.H1(
            children='Astrool-Weather',
            style={
                'textAlign': 'center'
            }
        ),
    html.H3(
            children='Minimal weather app for Astronomers in a hurry! ',
            style={
                'textAlign': 'center'
            }
        ),

    html.H3(
            children='Enter the city name of choice! and press Submit!',
            style={
                'textAlign': 'center'
            }
        ),
    dcc.Input(id='input-1-state', type='text', value='Mandi',style={
        'margin-left': '43%',
        'margin-right': 'auto'
    },),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.H3(
            children='Weather Report for the asked location: ',
            style={
                'textAlign': 'center'
            }
        ),
    html.Div(id='output-state'),
    html.P('     '),
    html.P('     '),
    html.Img(id='image',style={
        'margin-left': '47%',
        'margin-right': 'auto'
    },),
    html.P('     '),
    html.H3(id='output_we',
            style={
                'textAlign': 'center'
            }),
    html.P('     '),
    html.H2(id='output_we1',
            style={
                'textAlign': 'center'
            }),
    html.P('     '),
    # html.H2(style={'textAlign': 'center'}, children='Current Temperature:'),
    html.H2(id='temp',
            style={
                'textAlign': 'center',
                'color': 'blue'
            }),
    html.H2(id='precip',
            style={
                'textAlign': 'center',
                'color': 'red'
            }),
    html.H2(id='h',
            style={
                'textAlign': 'center',
                'color': 'green'
            }),
    html.H1(
            children='Visualisations to help understand: ',
            style={
                'textAlign': 'center'
            }
        ),
    html.H3(
            children='1) Plot of Variation of Temperature in a day : ',
            style={
                'textAlign': 'left',
                'margin-left': '30%',
                'color':'blue'
            }
        ),
    dcc.Graph(
        id='first_graph',
        style={'width': '50%',
               'margin-left':'26%'},
    ),
    html.H3(
            children='2) Plot of Variation of Cloud Cover in a day : ',
            style={
                'textAlign': 'left',
                'margin-left': '30%',
                'color':'blue'
            }
        ),
    dcc.Graph(
        id='first_graph1',
        style={'width': '50%',
               'margin-left':'26%'},
    ),
    html.H3(
            children='3) Plot of Variation of Precipitation Probability in a day : ',
            style={
                'textAlign': 'left',
                'margin-left': '30%',
                'color':'blue'
            }
        ),
    html.H4(
            children='You can go out taking your telescope on the time where the graph is at 0.',
            style={
                'textAlign': 'left',
                'margin-left': '30%',
                'color':'red'
            }
        ),
    dcc.Graph(
        id='first_graph2',
        style={'width': '50%',
               'margin-left':'26%'},
    ),
    html.H3(
            children='4) Plot of Variation of Precipitation Intensity in a day : ',
            style={
                'textAlign': 'left',
                'margin-left': '30%',
                'color':'blue'
            }
        ),
    dcc.Graph(
        id='first_graph3',
        style={'width': '50%',
               'margin-left':'26%'},
    ),
    html.H4(
            children='Credits: Akshita Jain - @akshita0208 on GitHub',
            style={
                'textAlign': 'center',
                'color':'red'
            }
        ),
    html.H4(
            children='Copyright © 2018 - Shreyas Bapat(@shreyasbapat) ',
            style={
                'textAlign': 'center',
                'color':'red'
            }
        ),
])


@app.callback(Output('output-state', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def update_output(n_clicks, input1):
    return ico(input1)

def ico(val):
    get_icon(weather_on(val))

def ret_str(val):
    return get_icon(weather_on(val))

def ret_sum(val):
    return get_summary(weather_on(val))

def ret_temp(val):
    return get_cur_temp(weather_latest(val))

def ret_pre(val):
    return get_cur_pro(weather_latest(val))

def ret_h(val):
    return get_cur_h(weather_latest(val))

def ret_tup(val):
    return get_data_24h(weather_on(val))

def ret_tup2(val):
    return get_data_24h_clo(weather_on(val))

def ret_tup3(val):
    return get_data_24h_pre(weather_on(val))

def ret_tup4(val):
    return get_data_24h_in(weather_on(val))

@app.callback(Output('image', 'src'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def update_image_src(n_clicks, value):
    image_filename = static_image_route + ret_str(value) + '.png'
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())

@app.callback(Output('output_we', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def update_msg1(n_clicks, value):
    stringo = ret_str(value)
    return stringo

@app.callback(Output('output_we1', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def update_msg(n_clicks, value):
    stringo = "Summary: " + ret_sum(value)
    return stringo

@app.callback(Output('temp', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def update_msg2(n_clicks, value):
    stringo = str(ret_temp(value))
    stringo = "Current Temperature: " + stringo + "℃"
    return stringo

@app.callback(Output('precip', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def update_msg3(n_clicks, value):
    stringo = str(ret_pre(value))
    stringo = "Probablilty of Rain: " + stringo
    return stringo

@app.callback(Output('h', 'children'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def update_msg4(n_clicks, value):
    stringo = str(ret_h(value))
    stringo = "Humidity: " + stringo
    return stringo

@app.callback(Output('first_graph', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def prin_gra(n_clicks, value):
    a,b = ret_tup(value)
    dict = {
        'data' : [
            {
                'x' : b,
                'y' : a,
                'name' : 'Temperature Data for 24 hours'
            }
        ]
    }
    return dict

@app.callback(Output('first_graph1', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def prin_gra1(n_clicks, value):
    a,b =  ret_tup2(value)
    dict = {
        'data' : [
            {
                'x' : b,
                'y' : a,
            }
        ]
    }
    return dict

@app.callback(Output('first_graph2', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def prin_gra1(n_clicks, value):
    a,b =  ret_tup3(value)
    dict = {
        'data' : [
            {
                'x' : b,
                'y' : a,
            }
        ]
    }
    return dict

@app.callback(Output('first_graph3', 'figure'),
              [Input('submit-button', 'n_clicks')],
              [State('input-1-state', 'value')])
def prin_gra1(n_clicks, value):
    a,b =  ret_tup4(value)
    dict = {
        'data' : [
            {
                'x' : b,
                'y' : a,
            }
        ]
    }
    return dict

if __name__ == '__main__':
    # Defining argparse argument for changing app port
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, help='Port to run the dash app, defaults to 8050')
    args = parser.parse_args()
    
    if args.port is None:
        app.run_server(debug=True)
    else:
        app.run_server(debug=True, port=args.port)
