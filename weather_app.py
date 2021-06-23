import os
import pytz
import pyowm
import streamlit as st
from datetime import datetime
from matplotlib import pyplot as plt
import plotly.graph_objects as go

from dotenv import load_dotenv

#-------------------------------------------------------------------------------
load_dotenv()
KEY = os.getenv('API_KEY')

#pyowm init
owm = pyowm.OWM(KEY)
manager = owm.weather_manager()

#streamlit - frontend application
st.title("5 Day Weather Forecast")
st.write("### Write the name of a City and select the Temperature Unit and Graph Type from the sidebar")
place = st.text_input("Enter name of the city :", "")

if place == None:
    st.write("Please enter a city")

temp_unit = st.selectbox("Select Temperature Unit", ("Celsius", "Fahrenheit"))
graph_type = st.selectbox("Select Graph Type", ("Line Graph", "Bar Graph"))

if temp_unit == 'Celsius':
    temp_unit = 'celsius'
else:
    temp_unit = 'fahrenheit'


def get_temp_details():
    dates = []
    min_temps = []
    max_temps = []

    obs = manager.forecast_at_place(place, '3h')
    place_forecast = obs.forecast

    for w in place_forecast:
        curr_day = datetime.utcfromtimestamp(w.reference_time())
        curr_date = curr_day.date()

        if curr_date not in dates:
            dates.append(curr_date)
            min_temps.append(None)
            max_temps.append(None)

        temp = w.temperature(temp_unit)['temp']

        if not min_temps[-1] or temp < min_temps[-1]:
            min_temps[-1] = temp
        if not max_temps[-1] or temp > max_temps[-1]:
            max_temps[-1] = temp

    return dates, min_temps, max_temps


#create bar or line graphs for visualisation
def create_bar_temp():
    days, min_temp, max_temp = get_temp_details()

    fig = go.Figure(data=[
        go.Bar(name='min temp', x=days, y=min_temp),
        go.Bar(name='max temp', x=days, y=max_temp)
    ])

    fig.update_layout(barmode='group')

    st.plotly_chart(fig)
    st.write("Min and Max Temperatures")


def create_line_temp():
    days, min_temp, max_temp = get_temp_details()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=min_temp, name='min temp'))
    fig.add_trace(go.Scatter(x=days, y=max_temp, name='max temp'))

    st.plotly_chart(fig)
    st.title("Min and Max Temperatures")


if __name__ == '__main__':

    if st.button("SUBMIT"):
        if graph_type == 'Bar Graph':
            create_bar_temp()
        else:
            create_line_temp()








