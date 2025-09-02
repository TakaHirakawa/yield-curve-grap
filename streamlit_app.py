import streamlit as st

st.title("Taka's yield curve graph")
st.write("Periods should be >1 month")
import pandas as pd
import numpy as np
import streamlit as st
import datetime as dt
import plotly
import plotly.express as px
import plotly.offline as plot
import plotly.graph_objs as go
import plotly.io as pio
import plotly.figure_factory as ff
from fredapi import Fred

fred_api = "07791adfe053b5c87cf0d6cc2cc0b3b3"
fred = Fred(fred_api)

#Getting Series

onem = pd.DataFrame(fred.get_series('GS1M'))
onem.reset_index(inplace = True)
onem = onem.rename(columns = {'index':'Date', 0: '1m'})

threem = pd.DataFrame(fred.get_series('GS3M'))
threem.reset_index(inplace = True)
threem = threem.rename(columns = {'index':'Date', 0: '3m'})
threem = threem[238:527]

sixm = pd.DataFrame(fred.get_series('GS6M'))
sixm.reset_index(inplace = True)
sixm = sixm.rename(columns = {'index':'Date', 0: '6m'})
sixm = sixm[238:527]

one = pd.DataFrame(fred.get_series('GS1'))
one.reset_index(inplace = True)
one = one.rename(columns = {'index':'Date', 0: '1Y'})
one = one[579:868]


two = pd.DataFrame(fred.get_series('GS2'))
two.reset_index(inplace = True)
two = two.rename(columns = {'index':'Date', 0: '2Y'})
two = two[301:590]

five = pd.DataFrame(fred.get_series('GS5'))
five.reset_index(inplace = True)
five = five.rename(columns = {'index':'Date', 0: '5Y'})
five = five[579:868]

seven = pd.DataFrame(fred.get_series('GS7'))
seven.reset_index(inplace = True)
seven = seven.rename(columns = {'index':'Date', 0: '7Y'})
seven = seven[384:673]

ten = pd.DataFrame(fred.get_series('GS10'))
ten.reset_index(inplace = True)
ten = ten.rename(columns = {'index':'Date', 0: '10Y'})
ten = ten[579:868]

twenty = pd.DataFrame(fred.get_series('GS20'))
twenty.reset_index(inplace = True)
twenty = twenty.rename(columns = {'index':'Date', 0: '20Y'})
twenty = twenty[579:868]

thirty = pd.DataFrame(fred.get_series('GS30'))
thirty.reset_index(inplace = True)
thirty = thirty.rename(columns = {'index':'Date', 0: '30Y'})
thirty = thirty[293:582]

#Cleaning up dataset

dfs = [onem.reset_index(), threem.reset_index(), sixm.reset_index(), 
       one.reset_index(), two.reset_index(), five.reset_index(), seven.reset_index(),
       ten.reset_index(), twenty.reset_index(), thirty.reset_index()]

df = pd.concat(dfs, axis = 1, join = 'outer')
df = df.drop(df['index'], axis = 1)
df = df.drop(df['Date'], axis = 1)
df = df.set_index(onem['Date'])

#Making the actual chart

date_range = st.slider(
    "Select date range: ",
    min_value = onem['Date'].min().to_pydatetime(),
    max_value = onem['Date'].min().to_pydatetime(),
    value =(onem['Date'].min().to_pydatetime(), onem['Date'].max().to_pydatetime()),
    format = "YYYY-MM-DD")

mask = (onem['Date'] >= date_range[0]) & (onem['Date'] <= date_range[1])
filtered_dates = onem['Date'][mask]


x = df.columns
y = df.index
z = df.to_numpy()

filtered_z = z[mask,:]

fig = go.Figure(data =[go.Surface(z=filtered_z, x=x, y=y)])
fig.update_layout(title = 'yield curves', 
                  scene = {"aspectratio": {"x":1, "y":1, "z": 0.4},
                           "xaxis": {"nticks":10}},
                  width = 1200, height = 800)

st.plotly_chart(fig, use_container_width = True, height = 2000)