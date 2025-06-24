from flask import Flask, render_template, request
import plotly.graph_objects as go
import plotly
from datetime import datetime, timedelta

app = Flask(__name__)

def generate_time_series(hour_interval=1):
    """Generate 24-hour time series data with specified interval"""
    now = datetime.now()
    time_points = [now + timedelta(hours=i) for i in range(0, 24, hour_interval)]
    values = [i**1.5 for i in range(len(time_points))]  # Sample data
    return time_points, values

def create_figure(mode='lines', graph_type='scatter', width=800, height=400, 
                 dark_mode=True, hour_interval=1, graph_id='mid'):
    # Generate time series data
    time_points, values = generate_time_series(hour_interval)
    
    if graph_type == 'bar':
        fig = go.Figure(go.Bar(x=time_points, y=values))
    else:
        fig = go.Figure(go.Scatter(x=time_points, y=values, mode=mode))
    
    # Theme colors
    bg_color = 'rgba(30, 30, 40, 0.7)' if dark_mode else 'rgba(240, 240, 250, 0.7)'
    text_color = '#ffffff' if dark_mode else '#333333'
    grid_color = 'rgba(255, 255, 255, 0.1)' if dark_mode else 'rgba(0, 0, 0, 0.1)'
    line_color = '#646cff' if dark_mode else '#3f51b5'
    
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        height=height,
        width=width,
        plot_bgcolor=bg_color,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=text_color),
        xaxis=dict(
            gridcolor=grid_color,
            type='date',
            tickformat='%H:%M',
            title='Time (24h)'
        ),
        yaxis=dict(gridcolor=grid_color),
        hoverlabel=dict(bgcolor=bg_color, font=dict(color=text_color))
    )
    # Update trace colors
    if graph_type == 'bar':
        fig.update_traces(marker=dict(color=line_color))
    else:
        fig.update_traces(line=dict(color=line_color))
    
    return fig

@app.route('/')
@app.route('/home')  # Add this if you want both URLs to work
def home():
    dark_mode = True
    return render_template('home.html', dark_mode=dark_mode)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    dark_mode = True
    hour_interval = int(request.form.get('hour_interval', 1)) if request.method == 'POST' else 1
    
    top_fig = create_figure(width=1800, height=750, dark_mode=dark_mode, graph_id='top')
    mid_fig = create_figure(
        mode='lines+markers', 
        width=1800, 
        height=720, 
        dark_mode=dark_mode,
        hour_interval=hour_interval,
        graph_id='mid'
    )
    bot_fig = create_figure(
        width=1800, 
        height=750, 
        dark_mode=dark_mode,
        hour_interval=hour_interval,
        graph_id='bot'
    )
    
    return render_template(
        'dashboard.html',
        top=plotly.io.to_json(top_fig),
        mid=plotly.io.to_json(mid_fig),
        bot=plotly.io.to_json(bot_fig),
        dark_mode=dark_mode,
        hour_interval=hour_interval
    )

@app.route('/set_mode/<mode>')
def set_mode(mode):
    dark_mode = True
    bot_fig = create_figure(mode=mode, width=1800, height=750, dark_mode=dark_mode)
    return plotly.io.to_json(bot_fig)

@app.route('/set_type/<graph_type>')
def set_type(graph_type):
    dark_mode = True
    bot_fig = create_figure(graph_type=graph_type, width=1800, height=750, dark_mode=dark_mode)
    return plotly.io.to_json(bot_fig)

if __name__ == '__main__':
    app.run(debug=True)