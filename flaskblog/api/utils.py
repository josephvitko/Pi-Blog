import requests


def get_temp():
    t = requests.get('http://192.168.1.249:5000/temp').text
    return t


def get_pressure():
    p = requests.get('http://192.168.1.249:5000/pressure').text
    return p


def get_humidity():
    h = requests.get('http://192.168.1.249:5000/humidity').text
    return h
