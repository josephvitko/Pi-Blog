from flask import Blueprint
from flaskblog import rest_api, db
from flask_restful import Resource, reqparse
from flaskblog.weather_data.models import Sensor, Data


weather_data = Blueprint('weather_data', __name__)

parser = reqparse.RequestParser()
parser.add_argument('sensor_name', required=True, help="sensor name cannot be blank")
parser.add_argument('value', type=float, required=True, help="value cannot be blank")


class DataAPI(Resource):
    def post(self):
        args = parser.parse_args()
        sensor = Sensor.query.filter_by(sensor_name=args['sensor_name']).first()
        value = args['value']
        data = Data(value=value, recorded_by=sensor)
        db.session.add(data)
        db.session.commit()
        print('data added:', sensor)
        return value, 201


sensor_parser = reqparse.RequestParser()
sensor_parser.add_argument('sensor_name', required=True, help="sensor name cannot be blank")
sensor_parser.add_argument('unit', required=True, help="unit cannot be blank")


class SensorAPI(Resource):
    def post(self):
        args = sensor_parser.parse_args()
        name = args['sensor_name']
        unit = args['unit']
        sensor = Sensor(name=name, unit=unit)
        db.session.add(sensor)
        db.session.commit()
        print('sensor created:', sensor)
        return name, 201
