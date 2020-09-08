import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import yfinance as yf 
import matplotlib.pyplot as plt

df_wide1 = yf.download("APT.AX ALC.AX ALU.AX APX.AX AMS.AX AD8.AX BTH.AX BVS.AX CAR.AX CAT.AX CL1.AX CDA.AX CPU.AX DTL.AX DHG.AX DUB.AX ELO.AX EML.AX FCL.AX HSN.AX IFM.AX IRI.AX IRE.AX KGN.AX 360.AX LNK.AX LVT.AX MP1.AX NEA.AX NET.AX NXT.AX OTW.AX PCK.AX PPS.AX PME.AX PPH.AX REA.AX RBL.AX RAP.AX RHP.AX TNE.AX CGL.AX VHT.AX WEB.AX WTC.AX XRO.AX",
                    start="2020-03-01", end="2020-08-25")
df_wide1 = df_wide1[['Close']]
df_wide1 = df_wide1.reset_index()
df = df_wide1=pd.melt(df_wide1, id_vars=['Date'])
#print(df_long.head(20))

# Initialize the app
dash_app = dash.Dash()
app = dash_app.server

def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list


dash_app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                    html.Div(className='four columns div-user-controls',
                             children=[
                                 html.H2('DASH ASX XTX TECH INDEX'),
                                 html.P('Visualising time series with Plotly - Dash.'),
                                 html.P('Pick one or more stocks from the dropdown below.'),
                                 html.Div(
                                     className='div-for-dropdown',
                                     children=[
                                         dcc.Dropdown(id='stockselector', options=get_options(df['variable_1'].unique()),
                                                      multi=True, value=[df['variable_1'].sort_values()[0]],
                                                      style={'backgroundColor': '#1E1E1E'},
                                                      className='stockselector'
                                                      ),
                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 dcc.Graph(id='timeseries', config={'displayModeBar': True}, animate=True)
                             ])
                              ])
        ]

)


# Callback for timeseries price
@dash_app.callback(Output('timeseries', 'figure'),
              [Input('stockselector', 'value')])
def update_graph(selected_dropdown_value):
    trace1 = []
    df_sub = df
    for stock in selected_dropdown_value:
        trace1.append(go.Scatter(x=df_sub[df_sub['variable_1'] == stock].Date,
                                 y=df_sub[df_sub['variable_1'] == stock]['value'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))
    traces = [trace1]
    data = [val for sublist in traces for val in sublist]
    data1={'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
    fig1=plt.scatter(1,2)
            
    figure = fig1
              

    return figure


if __name__ == '__main__':
   dash_app.run_server(debug=True)
