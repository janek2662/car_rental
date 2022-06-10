from datetime import date, datetime
from flask import Flask, session
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with, inputs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
import psycopg2

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
    __tablename__ = 'cars_table'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    version = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __init__(self, brand, version, year):
        self.brand = brand
        self.version = version
        self.year = year

    def __repr__(self):
        return '<id {}>'.format(self.id)
    

class UserModel(db.Model):
    __tablename__ = 'users_table'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    def __init__(self, login, password, is_admin):
        self.login = login
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ReservationModel(db.Model):
    __tablename__ = 'reservations_table'
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, nullable=False)
    date_from = db.Column(db.DateTime, nullable=False)
    date_to = db.Column(db.DateTime, nullable=False)
    
    def __init__(self, id, car_id, date_from, date_to):
        self.id = id
        self.car_id = car_id
        self.date_from = date_from
        self.date_to = date_to

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
        result = ReservationModel.query.filter_by(id=reservation_id).first()
        if not result:
            abort(404, message='Could not find reservation with that id...')
        return result
    
    @marshal_with(reservation_resource_fields)
    def post(self, reservation_id):
        args = reservation_post_args.parse_args()
        result = ReservationModel.query.filter_by(id=reservation_id).first()
        if result:
            abort(409, message='Reservation id taken...')
        reservation = ReservationModel(id=reservation_id, car_id=args['car_id'], date_from=args['date_from'], date_to=args['date_to'])
        db.session.add(reservation)
        db.session.commit()
        return reservation, 201

    @marshal_with(car_resource_fields)
    def patch(self, car_id):
        args = car_update_args.parse_args()
        result = CarModel.query.filter_by(id=car_id).first()
        if not result:
            abort(404, message='Reservation doesnt exist')

        if args['brand']:
            result.brand = args['brand']
        if args['version']:
            result.version = args['version']
        if args['year']:
            result.year = args['year']
        
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
