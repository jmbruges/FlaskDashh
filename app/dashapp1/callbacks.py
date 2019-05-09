from datetime import datetime as dt

import pandas_datareader as pdr
from dash.dependencies import Input
from dash.dependencies import Output

#Imports for data handling

import numpy as np
import ipywidgets as widgets
import scipy as sp
import scipy.io as spio # this is to import Matlab files, e.g. structure type
import plotly
import plotly.offline as py
import plotly.graph_objs as go
from plotly import tools

#Data handling

def loadmat(filename):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)

def _check_keys(dict):
    '''
    checks if entries in dictionary are mat-objects. If yes
    todict is called to change them to nested dictionaries
    '''
    for key in dict:
        if isinstance(dict[key], spio.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict        

def _todict(matobj):
    '''
    A recursive function which constructs from matobjects nested dictionaries
    '''
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, spio.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict
    
mat2 = loadmat('Sxs.mat')
sxallangles2 = mat2['Sx']



numang = len(sxallangles2)
s0 = []
s1 = []
s2 = []
s3 = []
data = []
figPC = []

#Layout for the figures

dispang = range(-90,95,5)
i = 0
for lists in sxallangles2:
    i=i+1
    #print(lists)
    s0 = np.array(sxallangles2[lists]['S0'])
    s1 = np.array(sxallangles2[lists]['S1'])
    s2 = np.array(sxallangles2[lists]['S2'])
    s3 = np.array(sxallangles2[lists]['S3'])
    
    s0P_r= ((s1[:,:,0]**2) + (s2[:,:,0]**2) + (s3[:,:,0]**2))**(1/2) #red component of angle 1
    s0P_g= ((s1[:,:,1]**2) + (s2[:,:,1]**2) + (s3[:,:,1]**2))**(1/2) #green component 
    s0P_b= ((s1[:,:,2]**2) + (s2[:,:,2]**2) + (s3[:,:,2]**2))**(1/2) #blue

    l = s0P_r.shape[0]*s0P_r.shape[1]

    xr = np.ravel(s1[:,:,0]/s0P_r)[1:l:20] #obS_S1_red
    yr = np.ravel(s2[:,:,0]/s0P_r)[1:l:20] #obS_S2_red
    zr = np.ravel(s3[:,:,0]/s0P_r)[1:l:20] #obS_S3_red

    xg = np.ravel(s1[:,:,1]/s0P_g)[1:l:20] #obS_S1_red
    yg = np.ravel(s2[:,:,1]/s0P_g)[1:l:20] #obS_S2_red
    zg = np.ravel(s3[:,:,1]/s0P_g)[1:l:20] #obS_S3_red

    xb = np.ravel(s1[:,:,2]/s0P_b)[1:l:20] #obS_S1_red
    yb = np.ravel(s2[:,:,2]/s0P_b)[1:l:20] #obS_S2_red
    zb = np.ravel(s3[:,:,2]/s0P_b)[1:l:20] #obS_S3_red
    
    trace0 = go.Scatter3d(
        x = xr,
        y = yr,
        z = zr,
        marker={'color': 'red', 'size': 1}, mode='markers', name='Red sensor'
    )
    
    trace1 = go.Scatter3d(
        x = xg,
        y = yg,
        z = zg,
        marker={'color': 'green', 'size': 1}, mode='markers', name='Green sensor'
    )
    
    trace2 = go.Scatter3d(
        x = xb,
        y = yb,
        z = zb,
        marker={'color': 'blue', 'size': 1}, mode='markers', name='Blue sensor'
    )
    
    layout = go.Layout(
        autosize=True,
        #width=300,
        #height=300,
        #margin=go.layout.Margin(
            #l=10,
            #r=10,
            #b=10,
            #t=10,
            #pad=20
        #),
        title = '<b>Poincare Sphere</b> {}'.format(dispang[i-1]),
        scene = dict(
        zaxis = dict(
            title = 'S3'
        ),
        yaxis = dict(
            title = 'S2'
        ),
        xaxis = dict(
            title = 'S1'
        ),)
    )
    data = [trace0, trace1, trace2]
    
    fig = go.Figure(data=data, layout=layout)
    figPC.append(fig)
    fig = None


def register_callbacks(dashapp):
    
    @dashapp.callback(Output('sphere-fig-angle', 'figure'),
    [Input('angle-detector', 'value')])
    def update_plot(angle):
        dff = figPC[dispang.index(angle)] 
        return {
        'data' :
            dff.data
            ,
        'layout' : 
            dff.layout
        }
        
   
    """@dashapp.callback(Output('angle', 'figure'), [Input('my-dropdown', 'value')])
    def update_graph(selected_dropdown_value):
        #df = pdr.get_data_yahoo(selected_dropdown_value, start=dt(2017, 1, 1), end=dt.now())
        dff = figPC[dispang.index(angle)] 
        return {
            'data' :
            dff.data
            ,
        'layout' : 
            dff.layout
        }
        """
        
