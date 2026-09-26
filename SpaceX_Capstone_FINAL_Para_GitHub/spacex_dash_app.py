import pandas as pd
import plotly.express as px
from dash import Dash,dcc,html,Input,Output

df=pd.read_csv('data/spacex_launch_dash.csv')
app=Dash(__name__)
app.layout=html.Div([
 html.H1('SpaceX Falcon 9 — Landing Success Dashboard'),
 dcc.Dropdown(id='site',options=[{'label':'All Sites','value':'All Sites'}]+[{'label':s,'value':s} for s in sorted(df['Launch Site'].dropna().unique())],value='All Sites'),
 dcc.RangeSlider(id='payload',min=float(df['Payload Mass (kg)'].min()),max=float(df['Payload Mass (kg)'].max()),value=[float(df['Payload Mass (kg)'].min()),float(df['Payload Mass (kg)'].max())],step=100),
 dcc.Graph(id='pie'),dcc.Graph(id='scatter')])
@app.callback(Output('pie','figure'),Output('scatter','figure'),Input('site','value'),Input('payload','value'))
def update(site,payload):
 d=df[df['Payload Mass (kg)'].between(payload[0],payload[1])].copy()
 if site!='All Sites': d=d[d['Launch Site']==site]
 return px.pie(d,names='class',title='Landing success'),px.scatter(d,x='Payload Mass (kg)',y='Flight Number',color='class',hover_data=['Booster Version'],title='Payload vs Flight Number')
if __name__=='__main__': app.run(debug=True)
