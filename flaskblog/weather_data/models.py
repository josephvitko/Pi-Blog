from datetime import datetime
import pytz
from flaskblog import db


class Sensor(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    unit = db.Column(db.String(50), nullable=True)
    data = db.relationship('Data', backref='recorded_by', lazy=True)

    def __repr__(self):
        return f"Sensor(''{self.id}', '{self.name}')"


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_recorded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    value = db.Column(db.Float(50), nullable=False)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensor.id'), nullable=False)

    def __repr__(self):
        return f"Data('{self.date_recorded}', '{self.value}', '{self.sensor_id}')"
