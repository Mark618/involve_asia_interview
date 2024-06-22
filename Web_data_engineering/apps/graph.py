from sre_parse import State
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import joblib
import pandas as pd
from app import app
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
import os

ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
print(ROOT_DIR)

d_path=ROOT_DIR+'/data/'
m_path=ROOT_DIR+'/model/'

df=pd.read_csv(d_path+"train.csv")
df=df.iloc[:,1:]
df_test= pd.read_csv(d_path+"test.csv")
df_test=df_test.iloc[:,1:]
scaler= joblib.load(m_path+"scaler.gz")
linear_model= joblib.load(m_path+"model.pkl")





fig=px.histogram(df['x1'], x="x1",color_discrete_sequence=px.colors.sequential.Mint_r, title='X1 distribution')
fig.update_layout(plot_bgcolor="#FFFFFF",
                   xaxis=dict(title=""),
                   yaxis=dict(title=""),
                   bargap=0.15
                   )

layout=html.Div(children=[
    html.Div(className='row', 
             children=[
                html.Div(className='card-panel', 
                         children=[
                            dcc.Graph(figure=fig)
                            ]
                         )
                ]
            ),
    html.Div(className='container row', 
             children=[
                html.Div(className='card-panel col l5', 
                         children=[
                             html.H5(className='', children='X1 value'),
                             dcc.Input(id="x1_input", type="number",value=0.3)
                            ]
                         ),
                html.Div(className='card-panel col l5', 
                         children=[
                             html.H5(className='', children='X2 value'),
                             dcc.Input(id="x2_input", type="number",value=0.5)
                            ]
                         ),
                html.Div(className='card-panel col l2', 
                         children=[
                             html.H5(className='', children='Y value'),
                             html.Div(id="Y value")
                            ]
                         ),
                ]
            ),   
    
])


@app.callback(
    Output('Y value','children'),     
    Input('x1_input','value'),
    Input('x2_input','value')
         
)
def updatevalue(x1_v,x2_v):
    temp_df= pd.DataFrame([[x1_v,x2_v,1]],columns=['x1','x2','y'])
    test_df=scaler.transform(temp_df)
    x_test=test_df[:,:2]
    y_val = linear_model.predict(x_test)
    test_df[:,-1]=y_val
    yval_revers=scaler.inverse_transform(test_df)   
    return yval_revers[:,-1]