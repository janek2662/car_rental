from datetime import date, datetime
from flask import Flask, session
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with, inputs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
import psycopg2
from dateutil.relativedelta import relativedelta
import datetime

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://user:password@localhost:5432/cars'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "secret"
db = SQLAlchemy(app)

#------------------------------------------------------------- DATABASE ---------------------------------------------------------------------------#
# def get_db_connection():
#     conn = psycopg2.connect(
#             host="localhost",
#             port=5432,
#             dbname='car_rental_db',
#             user='user',
#             password='password')
#     return conn
#------------------------------------------------------------- MODELS ---------------------------------------------------------------------------#

class CarModel(db.Model):
    __tablename__ = 'Cars_table1'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    version = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    reservation = db.relationship("Reservations_table1")

    def __init__(self, brand, version, year):
        self.brand = brand
        self.version = version
        self.year = year

    def __repr__(self):
        return '<id {}>'.format(self.id)
    

class UserModel(db.Model):
    __tablename__ = 'Users_table1'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    reservation = db.relationship("Reservations_table1")

    def __init__(self, login, password, is_admin):
        self.login = login
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ReservationModel(db.Model):
    __tablename__ = 'Reservations_table1'
    id = db.Column(db.Integer, primary_key=True)
    date_from = db.Column(db.DateTime, nullable=False)
    date_to = db.Column(db.DateTime, nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey("Cars_table1.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("Users_table1.id"), nullable=False)

    def __init__(self, car_id, date_from, date_to, user_id):
        self.date_from = date_from
        self.date_to = date_to
        self.car_id = car_id
        self.user_id = user_id

    def __repr__(self):
        return '<id {}>'.format(self.id)

db.create_all()

#-------------------------------------------------------- REQUEST PARSERS ------------------------------------------------------------------------#


# CAR
car_post_args = reqparse.RequestParser()
car_post_args.add_argument("brand", type=str, help="Brand of the car", required=True)
car_post_args.add_argument("version", type=int, help="Version of the car", required=True)
car_post_args.add_argument("year", type=int, help="Production year of the car", required=True)

# LOGIN/REGISTER
user_post_args = reqparse.RequestParser()
user_post_args.add_argument("login", type=str, help="Login of the user", required=True)
user_post_args.add_argument("password", type=str, help="Password of the user", required=True)
user_post_args.add_argument("is_admin", type=inputs.boolean, default=False)

#RESERVATION
reservation_post_args = reqparse.RequestParser()
reservation_post_args.add_argument("car_id", type=int, help="ID of the car", required=True)
reservation_post_args.add_argument("date_from", type=datetime, help="Login of the user", required=True)
reservation_post_args.add_argument("date_to", type=datetime, help="Password of the user", required=True)

reservation_update_args = reqparse.RequestParser()
reservation_update_args.add_argument("car_id", type=int, help="ID of the car update")
reservation_update_args.add_argument("date_from", type=datetime, help="Reservation date_from update")
reservation_update_args.add_argument("date_to", type=datetime, help="Reservation date_to update")

#-------------------------------------------------------- RESOURCE FIELDS (TO BE DISCUSSED AFTER ADDING DATABASE) ------------------------------------------------------------------------#

car_resource_fields = {
    'id': fields.Integer,
    'brand': fields.String,
    'version': fields.Integer,
    'year': fields.Integer
}

reservation_resource_fields = {
    'id': fields.Integer,
    'car_id': fields.Integer,
    'date_from': fields.DateTime(dt_format='rfc822'),
    'date_to': fields.DateTime(dt_format='rfc822')
}

user_resource_fields = {
    'id': fields.Integer,
    'login': fields.String,
    'password': fields.String,
    'is_admin': fields.Boolean(default=False)
}

#-------------------------------------------------------- RESOURCES ------------------------------------------------------------------------#
class Car(Resource):

    @marshal_with(car_resource_fields)
    def get(self, car_id):
        result = CarModel.query.filter_by(id=car_id).first()
        if not result:
            abort(404, message='Could not find car with that id...')

        return result
    
    @marshal_with(car_resource_fields)
    def post(self):
        if session["is_admin"]:
            args = car_post_args.parse_args()
            car = CarModel(brand=args['brand'], version=args['version'], year=args['year'])
            db.session.add(car)
            db.session.commit()
        else:
            abort(404, message='You need admin privilages...')

        return car, 201
    
    def delete(self, car_id):
        if session["is_admin"]:
            car = CarModel.query.filter_by(id=car_id).first()
            if not car:
                abort(404, message='Could not find car with that id...')
            db.session.delete(car)
            db.session.commit()
        else:
            abort(404, message='You need admin privilages...')
        
        return '', 204

class Reservation(Resource):

    @marshal_with(reservation_resource_fields)
    def get(self, reservation_id):
        if session["is_admin"]:
            result = ReservationModel.query.filter_by(id=reservation_id).first()
            if not result:
                abort(404, message='Could not find reservation with that id...')
        else:
            result = ReservationModel.query.filter_by(id=reservation_id).first()
            if not result.user_id == session["user_id"]:
                abort(404, message='Could not find reservation with that id... (debug: user is not allowed to see other reservations)')
                
        return result
    
    # CHECK WHETHER CAR IS AVAILABLE AT THAT DATE
    @marshal_with(reservation_resource_fields)
    def post(self):
        if not session["is_admin"] and session["user_id"]:
            args = reservation_post_args.parse_args()

            date_from = datetime.datetime.strptime(args['date_from'], "%Y-%m-%d").strftime("%d-%m-%Y")
            date_to = datetime.datetime.strptime(args['date_to'], "%Y-%m-%d").strftime("%d-%m-%Y")
            results = ReservationModel.query.filter_by(car_id=args['car_id']).all()
            for result in results:
                if date_to > result.date_from or date_from < result.date_to:
                    abort(404, message='Car is booked in that time...')

            if date_from > date_to:
                reservation = ReservationModel(date_from=args['date_from'], date_to=args['date_to'], car_id=args['car_id'], user_id=session["user_id"])
                db.session.add(reservation)
                db.session.commit()                
            else:
                abort(404, message='Dates are not right...')
        else:
            abort(404, message='Admin cannot make reservations...')

        return reservation, 201

    # reservation from cannot be after resertation to
    # CHECK WHETHER CAR IS AVAILABLE AT THAT DATE
    @marshal_with(reservation_resource_fields)
    def patch(self, reservation_id):
        if not session["is_admin"] and session["user_id"]:
            args = reservation_update_args.parse_args()
            result = ReservationModel.query.filter_by(id=reservation_id).first()

            if result.date_from != args['date_from'] or result.date_to != args['date_to'] or result.car_id != args['car_id']:
                abort(404, message='No changes being made...')

            date_from = datetime.datetime.strptime(args['date_from'], "%Y-%m-%d").strftime("%d-%m-%Y")
            date_to = datetime.datetime.strptime(args['date_to'], "%Y-%m-%d").strftime("%d-%m-%Y")
            results = ReservationModel.query.filter_by(car_id=args['car_id']).all()
            for result in results:
                if result.reservation_id == reservation_id:
                    continue
                if (date_to > result.date_from or date_from < result.date_to):
                    abort(404, message='Car is booked in that time...')

            if date_from > date_to:
                
                if args['date_from']:
                    result.date_from = args['date_from']
                if args['date_to']:
                    result.date_to = args['date_to']
                if args['car_id']:
                    result.car_id = args['car_id']

                # reservation = ReservationModel(date_from=args['date_from'], date_to=args['date_to'], car_id=args['car_id'], user_id=session["user_id"])
                db.session.add(result)
                db.session.commit()                
            else:
                abort(404, message='Dates are not right...')
        
        db.session.commit()
        return result
    
    def delete(self, car_id):
        del videos[car_id]
        return '', 204

class Login(Resource):
    
    @marshal_with(user_resource_fields)
    def post(self):
        args = user_post_args.parse_args()
        result = UserModel.query.filter_by(login=args['login']).first()

        if result.login == args['login'] and result.password == args['password']:
            session["is_admin"] = result.is_admin
            session["user_id"] = result.user_id
        else:
            abort(409, message='Bad credentials...')
        
        return result, 201

class Register(Resource):
    
    @marshal_with(user_resource_fields)
    def post(self):
        args = user_post_args.parse_args()
        result = UserModel.query.filter_by(login=args['login']).first()
        if result:
            abort(409, message='Login taken...')
        else:
            user = UserModel(login=args['login'], password=args['password'], is_admin=args['is_admin'])
            db.session.add(user)
            db.session.commit()

        return user, 201




#-------------------------------------------------------- API RESOURCES ------------------------------------------------------------------------#
api.add_resource(Login, "/login")
api.add_resource(Register, "/register")
api.add_resource(Reservation, "/reservation/<int:res_id>")
api.add_resource(Car, "/car/<int:car_id>")


#-------------------------------------------------------- MAIN ------------------------------------------------------------------------#
if __name__ == "__main__":
    app.run(debug=True)
