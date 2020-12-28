from flask import Blueprint
from flaskblog.api.utils import get_temp, get_pressure, get_humidity

api = Blueprint('api', __name__)


@api.route('/api/temp')
def temp():
    t = get_temp()
    return t


@api.route('/api/pressure')
def pressure():
    p = get_pressure()
    return p


@api.route('/api/humidity')
def humidity():
    h = get_humidity()
    return h
