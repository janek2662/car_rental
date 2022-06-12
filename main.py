from flask import Flask, session
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with, inputs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.hybrid import hybrid_property
import psycopg2
from dateutil.relativedelta import relativedelta
from datetime import datetime, time


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://user:password@localhost:5432/project'
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
    # __tablename__ = 'Cars_table1'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100), nullable=False)
    version = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    reservation = db.relationship('ReservationModel')

    def __init__(self, id, brand, version, year):
        self.id = id
        self.brand = brand
        self.version = version
        self.year = year

    def __repr__(self):
        return '<id {}>'.format(self.id)
    

class UserModel(db.Model):
    # __tablename__ = 'Users_table1'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    reservation = db.relationship('ReservationModel')

    def __init__(self, login, password, is_admin):
        self.login = login
        self.password = password
        self.is_admin = is_admin

    def __repr__(self):
        return '<id {}>'.format(self.id)

class ReservationModel(db.Model):
    # __tablename__ = 'Reservations_table1'
    id = db.Column(db.Integer, primary_key=True)
    date_from = db.Column(db.DateTime, nullable=False)
    date_to = db.Column(db.DateTime, nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey("car_model.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user_model.id"), nullable=False)

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
reservation_put_args = reqparse.RequestParser()
reservation_put_args.add_argument("car_id", type=int, help="ID of the car", required=True)
reservation_put_args.add_argument("date_from", type=str, help="GIVE ME DATETIME TYPE", required=True)
reservation_put_args.add_argument("date_to", type=str, help="GIVE ME DATETIME TYPE", required=True)

reservation_update_args = reqparse.RequestParser()
reservation_update_args.add_argument("car_id", type=int, help="ID of the car update")
reservation_update_args.add_argument("date_from", type=str, help="GIVE ME DATETIME TYPE")
reservation_update_args.add_argument("date_to", type=str, help="GIVE ME DATETIME TYPE")

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
    'date_from': fields.String,
    'date_to': fields.String
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

        return result, 200
    
    @marshal_with(car_resource_fields)
    def put(self, car_id):
        if session["is_admin"]:
            args = car_post_args.parse_args()
            car = CarModel.query.filter_by(id=car_id).first()
            if not car:            
                car = CarModel(id = car_id, brand=args['brand'], version=args['version'], year=args['year'])
                db.session.add(car)
                db.session.commit()
            else:
                abort(404, message='Car with such id already exists...')
        else:
            abort(403, message='You need admin privilages...')

        return car, 201
    
    def delete(self, car_id):
        if session["is_admin"]:
            car = CarModel.query.filter_by(id=car_id).first()
            if not car:
                abort(404, message='Could not find car with that id...')
            db.session.delete(car)
            db.session.commit()
        else:
            abort(403, message='You need admin privilages...')
        
        return '', 204

class Reservation(Resource):

    @marshal_with(reservation_resource_fields)
    def get(self, reservation_id):
        if session["is_admin"]:
            result = ReservationModel.query.filter_by(id=reservation_id).first()
            if result is None:
                abort(404, message='Could not find reservation with that id...')
        else:
            result = ReservationModel.query.filter_by(id=reservation_id).first()
            if result is None:
                abort(404, message='Could not find reservation with that id...')
            if not result.user_id == session["user_id"]:
                abort(403, message='Could not find reservation with that id... (debug: user is not allowed to see other reservations)')
                
        return result, 200


    @marshal_with(reservation_resource_fields)
    def patch(self, reservation_id):
        if not session["is_admin"] and session["user_id"]:
            args = reservation_update_args.parse_args()
            result = ReservationModel.query.filter_by(id=reservation_id).first()
            if result is None:
                abort(404, message='No reservation with this id...')
            try:
                date_from = datetime.strptime(args['date_from'], '%Y-%m-%d')
                date_to = datetime.strptime(args['date_to'], '%Y-%m-%d')
            except:
                abort(404, message='Bad datetime format...')

            if result.date_from == date_from and result.date_to == date_to and result.car_id == args['car_id']:
                abort(404, message='No changes being made...')

            results = ReservationModel.query.filter_by(car_id=args['car_id']).all()
            for result in results:
                if result.id == reservation_id:
                    continue
                if date_to > result.date_from or date_from < result.date_to:
                    abort(404, message='Car is booked in that time...')
            
            if  date_to > date_from:
                if args['date_from']:
                    result.date_from = args['date_from']
                if args['date_to']:
                    result.date_to = args['date_to']
                if args['car_id']:
                    result.car_id = args['car_id']

                db.session.add(result)
                db.session.commit()                
            else:
                abort(404, message='Dates are not right...')
        
        db.session.commit()
        return result, 200
    
    def delete(self, reservation_id):
        if session["user_id"]:
            result = ReservationModel.query.filter_by(id=reservation_id).first()
            if result is None:
                abort(404, message='No reservation with this id...')
            db.session.delete(result)
            db.session.commit()
        else:
            abort(403, message='You need to be logged in...')
        
        return '', 204

class ReservationPost(Resource):
        
    @marshal_with(reservation_resource_fields)
    def post(self):
        if not session["is_admin"] and session["user_id"]:
            args = reservation_put_args.parse_args()

            try:
                date_from = datetime.strptime(args['date_from'], '%Y-%m-%d')
                date_to = datetime.strptime(args['date_to'], '%Y-%m-%d')
            except:
                abort(404, message='Bad datetime format...')
      
            if date_to < date_from:
                abort(404, message='Dates are not correct')
            
            results = ReservationModel.query.filter_by(car_id=args['car_id']).all()
            for result in results:
                if (date_from >= result.date_from and date_from <= result.date_to) or (date_to >= result.date_from and date_to <= result.date_to) or (date_from <= result.date_from and date_to >= result.date_to):
                    abort(404, message='Car is booked in that time...')

            reservation = ReservationModel(date_from=args['date_from'], date_to=args['date_to'], car_id=args['car_id'], user_id=session["user_id"])
            db.session.add(reservation)
            db.session.commit()                
        else:
            abort(403, message='Admin cannot make reservations...')

        return reservation, 200

class Login(Resource):
    
    @marshal_with(user_resource_fields)
    def post(self):
        args = user_post_args.parse_args()
        result = UserModel.query.filter_by(login=args['login']).first()

        if result is None:
            abort(409, message='Bad credentials...')
        if result.login == args['login'] and result.password == args['password']:
            session["is_admin"] = result.is_admin
            session["user_id"] = result.id
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
api.add_resource(Reservation, "/reservation/<int:reservation_id>")
api.add_resource(ReservationPost, "/reservation")
api.add_resource(Car, "/car/<int:car_id>")


#-------------------------------------------------------- MAIN ------------------------------------------------------------------------#
if __name__ == "__main__":
    app.run(debug=True)
