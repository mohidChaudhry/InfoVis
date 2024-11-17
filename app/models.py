from app import db
from datetime import datetime


class SurveyResponse(db.Model):
    __tablename__ = 'survey_response'
    
    id = db.Column(db.Integer, primary_key=True)
    group_number = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    q1_time = db.Column(db.Integer)
    q1_closeness = db.Column(db.Integer)
    q1_data = db.Column(db.JSON)
    q2_time = db.Column(db.Integer)
    q2_closeness = db.Column(db.Integer)
    q2_data = db.Column(db.JSON)
    q3_time = db.Column(db.Integer)
    q3_closeness = db.Column(db.Integer)
    q3_data = db.Column(db.JSON)
    q4_time = db.Column(db.Integer)
    q4_closeness = db.Column(db.Integer)
    q4_data = db.Column(db.JSON)
    q5_time = db.Column(db.Integer)
    q5_closeness = db.Column(db.Integer)
    q5_data = db.Column(db.JSON)
    q6_time = db.Column(db.Integer)
    q6_closeness = db.Column(db.Integer)
    q6_data = db.Column(db.JSON)
    q7_time = db.Column(db.Integer)
    q7_closeness = db.Column(db.Integer)
    q7_data = db.Column(db.JSON)
    q8_time = db.Column(db.Integer)
    q8_closeness = db.Column(db.Integer)
    q8_data = db.Column(db.JSON)
    q9_time = db.Column(db.Integer)
    q9_closeness = db.Column(db.Integer)
    q9_data = db.Column(db.JSON)
    q10_time = db.Column(db.Integer)
    q10_closeness = db.Column(db.Integer)
    q10_data = db.Column(db.JSON)
    q11_time = db.Column(db.Integer)
    q11_closeness = db.Column(db.Integer)
    q11_data = db.Column(db.JSON)
    q12_time = db.Column(db.Integer)
    q12_closeness = db.Column(db.Integer)
    q12_data = db.Column(db.JSON)
    q13_time = db.Column(db.Integer)
    q13_closeness = db.Column(db.Integer)
    q13_data = db.Column(db.JSON)
    q14_time = db.Column(db.Integer)
    q14_closeness = db.Column(db.Integer)
    q14_data = db.Column(db.JSON)
    q15_time = db.Column(db.Integer)
    q15_closeness = db.Column(db.Integer)
    q15_data = db.Column(db.JSON)
    q16_time = db.Column(db.Integer)
    q16_closeness = db.Column(db.Integer)
    q16_data = db.Column(db.JSON)
    q17_time = db.Column(db.Integer)
    q17_closeness = db.Column(db.Integer)
    q17_data = db.Column(db.JSON)
    q18_time = db.Column(db.Integer)
    q18_closeness = db.Column(db.Integer)
    q18_data = db.Column(db.JSON)
    q19_time = db.Column(db.Integer)
    q19_closeness = db.Column(db.Integer)
    q19_data = db.Column(db.JSON)
    q20_time = db.Column(db.Integer)
    q20_closeness = db.Column(db.Integer)
    q20_data = db.Column(db.JSON)
    timestamp2 = db.Column(db.DateTime, default=datetime.utcnow)

        
        