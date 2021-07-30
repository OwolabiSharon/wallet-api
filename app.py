import os
from flask import Flask,jsonify
from flask_restful import Api,Resource
from resources.user import *
from flask_mysqldb import MySQL
from db import db
from flask_jwt_extended import JWTManager



#app = Flask(__name__)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://b846bafc1c95a2:630e7465@us-cdbr-east-03.cleardb.com/heroku_b31b5ece0f08b40'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '!@#$%^&*()_+=-0987654321'
app.config['PROPAGATE_EXCEPTIONS'] = True


api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def create_table():
    db.create_all()

api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(Account_balance, '/account_balance/<string:account_number>')
api.add_resource(Top__up, '/top__up')
api.add_resource(transfer, '/transfer')
api.add_resource(lookup, '/lookup')
api.add_resource(TransferHistory, '/transactions')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port =5000 , debug =True)
