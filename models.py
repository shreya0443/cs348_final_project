from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class Spirit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    threat_level = db.Column(db.String(10), nullable=False)  # Low, Medium, High
    status = db.Column(db.String(20), nullable=False, default="Active")  # Active, Exorcised
    reported_at = db.Column(db.DateTime, default=datetime.utcnow)

    location = db.relationship('Location', backref='spirits')
    __table_args__ = (
        db.Index('idx_spirit_location', 'location_id'),
        db.Index('idx_spirit_threat_status', 'threat_level', 'status'),
        db.Index('idx_spirit_reported', 'reported_at'),
    )


class Exorcist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    success_rate = db.Column(db.Float, nullable=False)

class ExorcismRequest(db.Model):
    __table_args__ = (
        db.Index('idx_request_spirit_status', 'spirit_id', 'status'),
    )    
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    spirit_id = db.Column(db.Integer, db.ForeignKey('spirit.id'), nullable=False)
    exorcist_id = db.Column(db.Integer, db.ForeignKey('exorcist.id'), nullable=True)
    status = db.Column(db.String(20), default="Pending")  # Pending, In Progress, Completed
    notes = db.Column(db.Text, nullable=True)
    request_date = db.Column(db.DateTime, default=datetime.utcnow)

    spirit = db.relationship('Spirit', backref='exorcism_requests')
    exorcist = db.relationship('Exorcist', backref='exorcism_requests')

    