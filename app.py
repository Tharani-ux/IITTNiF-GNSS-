# app.py
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

st.set_page_config(layout="wide", page_title="Forecasting Dashboard")

def generate_time_series(hour_interval=1):
    now = datetime.now()
    time_points = [now + timedelta(hours=i) for i in range(0, 24, hour_interval)]
    values = [i**1.5 for i in range(len(time_points))]
    return time_points, values

def create_figure(mode='lines', graph_type='scatter', width=None, height=400, dark_mode=True, hour_interval=1):
    time_points, values = generate_time_series(hour_interval)
    if graph_type == 'bar':
        fig = go.Figure(go.Bar(x=time_points, y=values, marker_color='#646cff' if dark_mode else '#3f51b5'))
    else:
        fig = go.Figure(go.Scatter(x=time_points, y=values, mode=mode, line=dict(color='#646cff' if dark_mode else '#3f51b5')))
    bg = 'rgba(30,30,40,0.7)' if dark_mode else 'rgba(240,240,250,0.7)'
    txt = '#fff' if dark_mode else '#333'
    grid = 'rgba(255,255,255,0.1)' if dark_mode else 'rgba(0,0,0,0.1)'
    fig.update_layout(
        plot_bgcolor=bg,
        paper_bgcolor='rgba(0,0,0,0)',
        font_color=txt,
        margin=dict(l=20,r=20,t=40,b=20),
        xaxis=dict(gridcolor=grid, tickformat='%H:%M', title='Time'),
        yaxis=dict(gridcolor=grid),
        height=height,
        width=width
    )
    return fig

# Sidebar controls
st.sidebar.header("Settings")
hour_interval = st.sidebar.slider("Hour interval", 1, 6, 1)
mode = st.sidebar.selectbox("Line mode", ['lines', 'markers', 'lines+markers'])
graph_type = st.sidebar.selectbox("Graph type", ['scatter', 'bar'])
dark_mode = st.sidebar.checkbox("Dark mode", True)

# Title
st.title("📈 Forecasting Dashboard")

# Main charts
top_fig = create_figure(mode, graph_type, height=300, hour_interval=1, dark_mode=dark_mode)
st.subheader("Top Chart")
st.plotly_chart(top_fig, use_container_width=True)

mid_fig = create_figure(mode, graph_type, height=300, hour_interval=hour_interval, dark_mode=dark_mode)
st.subheader("Middle Chart")
st.plotly_chart(mid_fig, use_container_width=True)

bot_fig = create_figure(mode, graph_type, height=300, hour_interval=hour_interval, dark_mode=dark_mode)
st.subheader("Bottom Chart")
st.plotly_chart(bot_fig, use_container_width=True)

# Optional: Export JSON for usage elsewhere
if st.sidebar.button("Export middle chart JSON"):
    st.download_button("Download JSON", data=json.dumps(mid_fig, default=str), file_name="mid_fig.json")
