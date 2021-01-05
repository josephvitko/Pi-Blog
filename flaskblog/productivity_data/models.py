from flaskblog import db
import math


class ProductivityData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    hours_prod = db.Column(db.Float, nullable=False)  # productive hours represented as a float
    hours_dist = db.Column(db.Float, nullable=False)  # unproductive hours represented as a float
    hours_total = db.column_property(hours_prod + hours_dist)

    def efficiency(self):
        return self.hours_prod / self.hours_total

    def output(self):
        return math.sqrt((self.hours_prod / 4.32) * self.efficiency())

    def __repr__(self):
        return f"Data('{self.date_recorded}', '{self.value}', '{self.sensor_id}')"
