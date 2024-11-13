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


def create_scatter_plot():
    file_path = os.path.join(app.root_path, '2018-2019_Daily_Attendance_20240429.csv')
    
    # Read and process data
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    df['Month'] = df['Date'].dt.strftime('%Y-%m')
    
    monthly_absences = df.groupby(['School Number', 'Month'])['Absent'].sum().reset_index()
    selected_schools = monthly_absences['School Number'].unique()[:10]
    
    filtered_absences = monthly_absences[
        monthly_absences['School Number'].isin(selected_schools)
    ].copy()
    
    # Convert School Number to string
    filtered_absences['School Number'] = filtered_absences['School Number'].astype(str)
    
    # Create figure
    fig = px.scatter(filtered_absences,
                    x='Month',
                    y='Absent',
                    color='School Number',
                    color_discrete_sequence=px.colors.qualitative.Set1,
                    title='Monthly Absences for 10 Schools',
                    labels={'Absent': 'Total Absences', 'Month': 'Month'},
                    height=600,
                    custom_data=['School Number'])  # Explicitly specify custom_data
    
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
        hovertemplate='School: %{customdata[0]}<br>Month: %{x}<br>Absences: %{y:,.0f}<extra></extra>'
    )
    
    # Convert to JSON for passing to template
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def create_heat_map():
    # Update this path to match your CSV file location in your project
    file_path = os.path.join(app.root_path, '2018-2019_Daily_Attendance_20240429.csv')
        
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    df['Month'] = df['Date'].dt.strftime('%Y-%m')
    
    monthly_absences = df.groupby(['School Number', 'Month'])['Absent'].sum().reset_index()
    selected_schools = monthly_absences['School Number'].unique()[:10]
    filtered_absences = monthly_absences[monthly_absences['School Number'].isin(selected_schools)]
    
    # Create pivot table
    absence_pivot = filtered_absences.pivot(
        index='School Number', 
        columns='Month', 
        values='Absent'
    ).fillna(0)
    
    # Create figure using px.imshow which handles axes differently
    fig = px.imshow(
        absence_pivot,
        labels=dict(x="Month", y="School", color="Total Absences"),
        color_continuous_scale='Plasma',
        aspect='auto'
    )

    y_positions = list(range(1, (len(absence_pivot.index)+1)))
    
    # Update layout
    fig.update_layout(
        title='Monthly Absences of 10 Schools',
        xaxis=dict(
            tickangle=45,
            side='bottom'
        ),
        yaxis=dict(
            tickmode='array',
            ticktext=list(absence_pivot.index),  # School DBNs
            tickvals=y_positions,  # Position values starting from 0
            side='left',
            autorange='reversed'  # Keep schools in original order
        ),
        margin=dict(t=50, l=200),
        height=600,
        template='plotly_white'
    )
    
    # Disable hover
    fig.update_traces(hoverinfo='none')
    
    # Convert to JSON for passing to template
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

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

    if args[1].strip() == "heat":
        plot_json = create_heat_map()
        return render_template(
            "heat.html",
            plot_json=plot_json
        )
    elif args[1].strip() == "scatter":
        plot_json = create_scatter_plot()
        return render_template(
            "scatter.html",
            plot_json=plot_json
        )