import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
import geocoder
from datetime import datetime
import forecastio
from dash.dependencies import Input, Output, State


def weather_on(loca):
    a = geocoder.location(location=loca)
    api_key = "c5dde0bafce3442350c75b743864339a"
    lat = a.latlng[0]
    lng = a.latlng[1]
    forecast = forecastio.load_forecast(api_key, lat, lng, time=datetime.now())
    byHour = forecast.hourly()
    return byHour

def get_icon(byhour):
    return byhour.icon

def get_summary(byhour):
    return byhour.summary

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
    stringo = ret_sum(value)
    return stringo


if __name__ == '__main__':
    app.run_server(debug=True)
