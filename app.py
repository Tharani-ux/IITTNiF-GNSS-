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

def create_figure(mode='lines', graph_type='scatter', dark_mode=True, hour_interval=1, title=""):
    time_points, values = generate_time_series(hour_interval)
    
    # Color schemes for both modes
    colors = {
        'dark': {
            'bg': 'rgba(20, 20, 30, 0.9)',
            'plot_bg': 'rgba(30, 30, 50, 0.7)',
            'text': '#ffffff',
            'grid': 'rgba(255, 255, 255, 0.1)',
            'accent': '#646cff',
            'secondary': '#ff7de9',
            'highlight': '#ffcc00'
        },
        'light': {
            'bg': 'rgba(240, 240, 250, 0.9)',
            'plot_bg': 'rgba(255, 255, 255, 0.7)',
            'text': '#333333',
            'grid': 'rgba(0, 0, 0, 0.1)',
            'accent': '#3f51b5',
            'secondary': '#ff5252',
            'highlight': '#ff9800'
        }
    }
    
    theme = colors['dark'] if dark_mode else colors['light']
    
    if graph_type == 'bar':
        fig = go.Figure(go.Bar(
            x=time_points, 
            y=values, 
            marker_color=theme['accent'],
            marker_line_color=theme['secondary'],
            marker_line_width=1.5,
            opacity=0.8
        ))
    else:
        fig = go.Figure(go.Scatter(
            x=time_points, 
            y=values, 
            mode=mode,
            line=dict(
                color=theme['accent'],
                width=3,
                shape='spline',
                smoothing=1.3
            ),
            marker=dict(
                size=8,
                color=theme['secondary'],
                line=dict(
                    width=2,
                    color=theme['highlight']
                )
            ),
            fill='tozeroy' if 'lines' in mode else None,
            fillcolor=f'rgba(100, 108, 255, {0.2 if dark_mode else 0.1})'
        ))
    
    # Find max value for annotation
    max_val = max(values)
    max_time = time_points[values.index(max_val)]
    
    fig.update_layout(
        title={
            'text': f"<b>{title}</b>",
            'y':0.95,
            'x':0.05,
            'xanchor': 'left',
            'yanchor': 'top',
            'font': {
                'size': 24,
                'color': theme['accent']
            }
        },
        plot_bgcolor=theme['plot_bg'],
        paper_bgcolor=theme['bg'],
        font_color=theme['text'],
        margin=dict(l=50, r=50, t=80, b=50),
        xaxis=dict(
            gridcolor=theme['grid'],
            tickformat='%H:%M',
            title='Time',
            showline=True,
            linecolor=theme['grid'],
            linewidth=2,
            mirror=True
        ),
        yaxis=dict(
            gridcolor=theme['grid'],
            showline=True,
            linecolor=theme['grid'],
            linewidth=2,
            mirror=True
        ),
        height=700,
        hovermode="x unified",
        showlegend=False,
        annotations=[
            dict(
                x=max_time,
                y=max_val,
                xref="x",
                yref="y",
                text=f"Peak: {max_val:.1f}",
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40,
                bgcolor=theme['highlight'],
                opacity=0.8,
                font=dict(
                    color=theme['bg'],
                    size=12
                )
            )
        ]
    )
    
    # Add range slider
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1h", step="hour", stepmode="backward"),
                dict(count=6, label="6h", step="hour", stepmode="backward"),
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(step="all")
            ]),
            bgcolor=theme['plot_bg'],
            activecolor=theme['accent'],
            font=dict(color=theme['text'])
        )
    )
    
    # Add hover effects
    fig.update_traces(
        hovertemplate="<b>Time:</b> %{x|%H:%M}<br><b>Value:</b> %{y:.2f}<extra></extra>",
        hoverlabel=dict(
            bgcolor=theme['accent'],
            font_size=14,
            font_color=theme['text']
        )
    )
    
    return fig

# Sidebar controls with improved styling
with st.sidebar:
    st.markdown("""
    <style>
    .sidebar .sidebar-content {
        background-color: #1a1a2e;
        color: white;
    }
    .stSlider > div > div > div > div {
        background-color: #646cff !important;
    }
    .stSelectbox > div > div > div > div {
        background-color: #1a1a2e !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.header("⚙️ Dashboard Settings")
    hour_interval = st.slider("Hour interval", 1, 6, 1, 
                            help="Select the time interval between data points")
    mode = st.selectbox("Line mode", ['lines', 'markers', 'lines+markers'],
                      help="Choose how to display the data points")
    graph_type = st.selectbox("Graph type", ['scatter', 'bar'],
                            help="Select between line chart or bar chart")
    dark_mode = st.checkbox("Dark mode", True,
                          help="Toggle between dark and light theme")

# Title with custom styling
st.markdown("""
<h1 style='text-align: center; color: #646cff; font-weight: 800; 
            border-bottom: 2px solid #646cff; padding-bottom: 10px;'>
    📈 Advanced Forecasting Dashboard
</h1>
""", unsafe_allow_html=True)

# Create tabs for each graph with custom styling
tab1, tab2, tab3 = st.tabs(["📊 Top Chart", "📈 Middle Chart", "📉 Bottom Chart"])

with tab1:
    top_fig = create_figure(
        mode, graph_type, 
        hour_interval=1, 
        dark_mode=dark_mode,
        title="Real-time Performance Metrics"
    )
    st.plotly_chart(top_fig, use_container_width=True)

with tab2:
    mid_fig = create_figure(
        mode, graph_type, 
        hour_interval=hour_interval, 
        dark_mode=dark_mode,
        title="Detailed Trend Analysis"
    )
    st.plotly_chart(mid_fig, use_container_width=True)
    
    # Export button with better styling
    if st.button("💾 Export Middle Chart Data", 
                help="Download the middle chart data as JSON"):
        st.download_button(
            label="⬇️ Download JSON",
            data=json.dumps(mid_fig, default=str),
            file_name="trend_analysis.json",
            mime="application/json",
            key="download-json"
        )

with tab3:
    bot_fig = create_figure(
        mode, graph_type, 
        hour_interval=hour_interval, 
        dark_mode=dark_mode,
        title="Forecast Projections"
    )
    st.plotly_chart(bot_fig, use_container_width=True)

# Enhanced CSS styling for the entire app
st.markdown("""
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        margin-bottom: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 25px;
        margin: 0;
        background-color: rgba(100, 108, 255, 0.1);
        border-radius: 8px 8px 0 0 !important;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(100, 108, 255, 0.2) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(100, 108, 255, 0.3) !important;
        color: #646cff !important;
        font-weight: 600;
        box-shadow: 0 4px 8px rgba(100, 108, 255, 0.2);
    }
    
    /* Button styling */
    .stButton>button {
        border: 2px solid #646cff;
        border-radius: 8px;
        color: #646cff;
        background-color: rgba(100, 108, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        color: white !important;
        background-color: #646cff !important;
        border-color: #535bf2 !important;
    }
    
    /* Plotly chart styling */
    .stPlotlyChart {
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
    }
    
    .stPlotlyChart:hover {
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)