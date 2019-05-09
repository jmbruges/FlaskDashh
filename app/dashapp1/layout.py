import dash_core_components as dcc
import dash_html_components as html


dispang = range(-90,95,5)

layout = html.Div([
    
    html.Div([
        dcc.Graph(
            id='sphere-fig-angle',
            style={"max-width": "1000px", "margin": "auto"}#,{'width': '40%', 'float': 'center','autosizable', 'display': 'inline-block'}
        #hoverData={'points': [{'customdata': 'Japan'}]}
        )
    ]),
    
    #html.Div(
    dcc.Slider(
        id='angle-detector',
        min=-90,
        max=90,
        step=5,
        value=0,
        marks={i: '{}'.format(i) for i in dispang}
    #marks={str(year): str(year) for year in df['Year'].unique()}
    )
],style={'width': '90%', 'float' : 'center'})

