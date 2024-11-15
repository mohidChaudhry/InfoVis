from flask import (
    render_template, flash, request, session, redirect, url_for, jsonify
)
from app import app, models, db
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils  # Add this import
import pandas as pd
import json
import numpy as np


def generate_synthetic_data(num_schools=10, start_date='2023-09', periods=10):
    
    # Generate date range
    dates = pd.date_range(start=start_date, periods=periods, freq='M')
    months = [date.strftime('%Y-%m') for date in dates]
    
    # Create empty lists to store data
    data = []
    
    for school in range(1, num_schools + 1):
        # Generate a base absence rate for each school (between 20 and 50)
        base_absence_rate = np.random.randint(30, 70)
        
        # Generate monthly variations
        for month in months:
            # Add some random variation to the base rate (±30%)
            variation = np.random.uniform(-0.3, 0.3)
            absences = int(base_absence_rate * (1 + variation))
            
            data.append({
                'School Number': str(school),
                'Month': month,
                'Absent': absences
            })
    
    return pd.DataFrame(data)

def create_scatter_plot(data=None):
    if data is None:
        data = generate_synthetic_data()
    
    # Create figure
    fig = px.scatter(data,
                    x='Month',
                    y='Absent',
                    color='School Number',
                    color_discrete_sequence=px.colors.qualitative.Set1,
                    title='Monthly Absences for 10 Schools',
                    labels={'Absent': 'Total Absences', 'Month': 'Month'},
                    height=600,
                    custom_data=['School Number'])
    
    # Update layout for better readability
    fig.update_layout(
        hovermode='closest',
        legend=dict(
            title='School Number',
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        ),
        xaxis=dict(
            type='category',
            tickangle=45,
            categoryorder='category ascending'
        ),
        margin=dict(r=200),
        template='plotly_white'
    )
    
    # Update traces with hover template
    fig.update_traces(
        marker=dict(
            size=15,
            line=dict(width=2, color='white'),
            symbol='circle',
            opacity=0.8
        ),
        hovertemplate=None,
        hoverinfo='none'
    )
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

def create_heat_map(data=None):
    """Create heat map from either provided or generated data"""
    if data is None:
        data = generate_synthetic_data()

    
    # Convert School Number to numeric type
    data['School Number'] = pd.to_numeric(data['School Number'])

    month_order = ['2023-09', '2023-10', '2023-11', '2023-12', '2024-01', '2024-02', '2024-03', '2024-04', '2024-05', '2024-06']

    # Create pivot table with sorted index
    absence_pivot = data.pivot(
    index='School Number',
    columns='Month', 
    values='Absent'
    )[month_order].sort_index().fillna(0)
    
    # Create figure
    fig = px.imshow(
        absence_pivot,
        labels=dict(x="Month", y="School", color="Total Absences"),
        color_continuous_scale='Plasma',
        aspect='auto',
        x=month_order
    )
    
    y_positions = list(range(1,11))
    
    # Update layout
    fig.update_layout(
        title='Monthly Absences of 10 Schools',
        xaxis=dict(
            type='category',
            tickangle=45,
            side='bottom',
            ticktext=month_order,
            tickvals=list(range(len(month_order))),
            tickmode='array'
        ),
        
        yaxis=dict(
            tickmode='array',
            ticktext=list(absence_pivot.index),
            tickvals=y_positions,
            side='left',
            autorange='reversed'
        ),
        margin=dict(t=50, l=200),
        height=600,
        template='plotly_white'
    )
    
    # Disable hover
    fig.update_traces(hoverinfo='none', hovertemplate=None)
    
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

# Home page
@app.route('/', methods=["GET", "POST"])
def home():
    return render_template(
        "home.html"
    )

# Information sheet page
@app.route('/info', methods=["GET", "POST"])
def info():
    return render_template(
        "info.html"
    )

# Information sheet page
@app.route('/contact', methods=["GET", "POST"])
def contact():
    return render_template(
        "contact.html"
    )

@app.route('/survey/<int:qid>', methods=["GET", "POST"])
def survey(qid):
    args = []
    with open(os.path.join(app.root_path, 'questions1'), 'r') as file:
        for line in file:
            args = line.split(" ")
            if args[0] == str(qid):
                break

    data = generate_synthetic_data()

    if args[1].strip() == "heat":
        plot_json = create_heat_map(data)
        return render_template(
            "heat.html",
            plot_json=plot_json
        )
    elif args[1].strip() == "scatter":
        plot_json = create_scatter_plot(data)
        return render_template(
            "scatter.html",
            plot_json=plot_json
        )