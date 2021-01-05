from flask import Blueprint, render_template
from flaskblog import rest_api, db
from flask_restful import Resource, reqparse, inputs
from flaskblog.productivity_data.models import ProductivityData


productivity_data = Blueprint('productivity_data', __name__)

parser = reqparse.RequestParser()
parser.add_argument('date', type=inputs.date, required=True, help="sensor name cannot be blank")
parser.add_argument('prod_hours', type=float, required=True)  # number of hours as a float
parser.add_argument('dist_hours', type=float, required=True)  # number of hours as a float


class ProductivityDataAPI(Resource):
    def post(self):
        args = parser.parse_args()
        input_date = args['date'].date()
        p_data = ProductivityData.query.filter_by(date=input_date).first()
        if p_data is None:
            pd = ProductivityData(date=input_date, hours_prod=args['prod_hours'], hours_dist=args['dist_hours'])
            db.session.add(pd)
        else:
            p_data.hours_prod = args['prod_hours']
            p_data.hours_dist = args['dist_hours']
        db.session.commit()
        print('data added:', input_date)
        return str(input_date), 201
