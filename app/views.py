from flask import Blueprint, render_template, flash, request, session, redirect, url_for, jsonify
from app import models, db
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from app.models import SurveyResponse
import plotly.express as px
import plotly.graph_objects as go
import plotly.utils  
import pandas as pd
import json
import numpy as np



main = Blueprint('main', __name__)

def get_question_file(survey_id):
    """
    Determines which question file to use based on survey_id
    Group 1 (odd survey_ids): questions1 (Heat->Scatter)
    Group 2 (even survey_ids): questions2 (Scatter->Heat)
    """
    return 'questions1' if survey_id % 2 == 1 else 'questions2'

def get_group_number(survey_id):
    """Returns 1 for odd survey_ids, 2 for even survey_ids"""
    return 1 if survey_id % 2 == 1 else 2

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

def create_heat_map(data=None):
    """Create heat map from either provided or generated data"""
    if data is None:
        data = generate_synthetic_data()
    
    # Create a copy of the data to avoid modifying the original
    data_copy = data.copy()
    
    # Convert School Number to numeric type only for this function
    data_copy['School Number'] = pd.to_numeric(data_copy['School Number'])

    month_order = ['2023-09', '2023-10', '2023-11', '2023-12', '2024-01', 
                   '2024-02', '2024-03', '2024-04', '2024-05', '2024-06']

    # Create pivot table with sorted index
    absence_pivot = data_copy.pivot(
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

def create_scatter_plot(data=None):
    if data is None:
        data = generate_synthetic_data()
    
    # Create a copy of the data to avoid modifying the original
    data_copy = data.copy()
    
    # Ensure School Number is treated as categorical
    data_copy['School Number'] = data_copy['School Number'].astype(str)
    
    # Create figure
    fig = px.scatter(data_copy,
        x='Month',
        y='Absent',
        color='School Number',
        color_discrete_sequence=px.colors.qualitative.Set1,
        category_orders={"School Number": [str(i) for i in range(1, 11)]},
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

# Home page
@main.route('/', methods=["GET", "POST"])
def home():
    return render_template(
        "home.html"
    )

# Information sheet page
@main.route('/info', methods=["GET", "POST"])
def info():
    return render_template(
        "info.html"
    )

# Information sheet page
@main.route('/contact', methods=["GET", "POST"])
def contact():
    return render_template(
        "contact.html"
    )
data = None

@main.route('/start_survey', methods=['POST'])
def start_survey():
    last_survey = SurveyResponse.query.order_by(SurveyResponse.id.desc()).first()
    next_id = 1 if not last_survey else last_survey.id + 1
    
    new_survey = SurveyResponse()
    new_survey.id = next_id
    db.session.add(new_survey)
    new_survey.group_number = get_group_number(next_id)
    db.session.commit()
    
    session['survey_id'] = new_survey.id
    session['group_number'] = new_survey.group_number
    session['start_time'] = datetime.now().timestamp()
    return redirect(url_for('main.survey', qid=1))

def calculate_monthly_totals(data):
    """Calculate total absences for each month and return sorted months by total absences"""
    monthly_totals = data.groupby('Month')['Absent'].sum().reset_index()
    print("\n--- Monthly Totals Before Sorting ---")
    print(monthly_totals)
    
    monthly_totals = monthly_totals.sort_values('Absent', ascending=False)
    print("\n--- Monthly Totals After Sorting ---")
    print(monthly_totals)
    
    ordered_months = monthly_totals['Month'].tolist()
    print("\n--- Final Ordered Months (from highest to lowest absences) ---")
    for i, month in enumerate(ordered_months, 1):
        print(f"{i}. {month} - {monthly_totals[monthly_totals['Month'] == month]['Absent'].values[0]} absences")
    
    return ordered_months

def calculate_closeness(user_answer, correct_order):
    """Calculate closeness score (1-10) based on answer position"""
    print("\n--- Calculating Closeness Score ---")
    print(f"User selected month: {user_answer}")
    print(f"Correct order of months: {correct_order}")
    
    try:
        position = correct_order.index(user_answer) + 1
        closeness = min(position, 10)
        print(f"Position of selected month: {position}")
        print(f"Closeness score: {closeness}")
        return closeness
    except ValueError:
        print(f"Selected month {user_answer} not found in correct order")
        return 10

@main.route('/survey/<int:qid>', methods=["GET", "POST"])
def survey(qid):

    if qid == 1 and 'survey_id' not in session:
        return redirect(url_for('main.home'))
    
    global data
    
    end_time = datetime.now().timestamp()
    if 'start_time' in session:
        time_taken = int(end_time - session['start_time'])
        record = SurveyResponse.query.get(session['survey_id'])
        if record and qid > 1: 
            setattr(record, f'q{qid-1}_time', time_taken)
            
            try:
                clicked_data = json.loads(request.form.get('clicked_data', '{}'))
                print(f"Received clicked data for question {qid-1}: {clicked_data}")
                
                if clicked_data and 'Month' in clicked_data:
                    correct_order = session.get('current_correct_order', [])
                    print(f"Using correct order for question {qid-1}: {correct_order}")
                    
                    user_month = clicked_data['Month']
                    print(f"User selected month for question {qid-1}: {user_month}")
                    
                    closeness = calculate_closeness(user_month, correct_order)
                    print(f"Calculated closeness score for question {qid-1}: {closeness}")
                    
                    setattr(record, f'q{qid-1}_closeness', closeness)

                    if data is not None:
                        data_dict = data.to_dict(orient='records')
                        setattr(record, f'q{qid-1}_data', data_dict)
                        
                else:
                    print(f"No Month data in clicked_data for question {qid-1}")
            except json.JSONDecodeError as e:
                print(f"Error decoding clicked data for question {qid-1}: {e}")
            except Exception as e:
                print(f"Error processing clicked data for question {qid-1}: {e}")
            
            try:
                db.session.commit()
                print(f"Successfully committed question {qid-1} data to database")
            except Exception as e:
                print(f"Database error for question {qid-1}: {e}")
                db.session.rollback()
    
    if qid == 21:
        session.pop('survey_id', None)
        session.pop('start_time', None)
        session.pop('current_correct_order', None)
        return render_template("end.html")

    if qid % 2 == 1:
        data = generate_synthetic_data()
        correct_order = calculate_monthly_totals(data)
        session['current_correct_order'] = correct_order
        print(f"Generated new data for questions {qid}&{qid+1}. Correct order: {correct_order}")
    else:
        if data is None:
            print(f"Warning: Data missing for question {qid}, regenerating...")
            data = generate_synthetic_data()
            correct_order = calculate_monthly_totals(data)
            session['current_correct_order'] = correct_order
            print(f"Regenerated data for question {qid} (fallback). Correct order: {correct_order}")
        else:
            print(f"Using existing data for question {qid}")
    
    session['start_time'] = datetime.now().timestamp()

    args = []
    question_file = get_question_file(session['survey_id'])
    with open(os.path.join(main.root_path, question_file), 'r') as file:
        for line in file:
            args = line.split(" ")
            if args[0] == str(qid):
                break

    if args[1].strip() == "heat":
        plot_json = create_heat_map(data)
        return render_template(
            "heat.html",
            qid_n = int(qid) + 1,
            plot_json=plot_json
        )
    elif args[1].strip() == "scatter":
        plot_json = create_scatter_plot(data)
        return render_template(
            "scatter.html",
            qid_n = int(qid) + 1,
            plot_json=plot_json
        )