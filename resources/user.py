import random
from db import db
from models.user import *
from flask import jsonify
from flask_restful import Resource, reqparse, inputs
from flask_jwt_extended import create_access_token,jwt_required


# all endpoint responses are to be called from a function or from a dictionary key value pair thingy
#ill do it later😁

def returnfunc(status,data,message):
    return {
        'status': status,
        'data': data,
        'message': message
    }



class Register(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        'first_name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'middle_name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'last_name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'date_of_birth',
        type=inputs.datetime_from_iso8601,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument(
        'pin',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    def post(self):
        data = Register.parser.parse_args()

        #def encrypt_string(hash_string):
        #    sha_signature = \
        #    hashlib.sha256(hash_string.encode()).hexdigest()
        #    return sha_signature

        if User.find_by_email(data['email']):
            response = returnfunc(False,None,'user exists allready')
            return response,400

        list=random.sample(range(1000000000000), 1)
        number = random.choice(list)
        user = User(
            number,#to be randomly generated some way or the other later,
            data['first_name'],
            data['middle_name'],
            data['last_name'],
            data['date_of_birth'],
            data['password'],
            data['email'],
            data['pin'],
            '00'
        )
        #user.password = register.encrypt_string(user.password)
        #user.pin = register.encrypt_string(user.pin)
        User.save_to_db(user)
        response = returnfunc(True,user.json(),'user created succesfully')
        return response,200



class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
            'account_number',
            type=str,
            required=True,
            help="This field cannot be left blank!"
                       )
    parser.add_argument(
            'password',
            type=str,
            required=True,
            help="This field cannot be left blank!"
                        )
    def post(self):
        data = Login.parser.parse_args()
        user = User.find_by_account_number(data['account_number']) and User.find_by_password(data['password'])

        if user:
            access_token = create_access_token(identity=user.id,fresh =True)
            response = returnfunc(True,access_token,'you are logged in')
            return response,200
        response = returnfunc(False,None,'user not found')
        return response,404




class Account_balance(Resource):
    @jwt_required()
    def get(self, account_number):
        user = User.find_by_account_number(account_number)
        balance = user.account_balance
        #user =user.phone_number[x.json() for x in Received_Transfer.query.all()]
        if user:
            response = returnfunc(True,balance,'this is your account_number')
            return response,200

        response = returnfunc(False,None,'user not found')
        return response,404



class Top__up(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'account_number',
        type=str,
        required=True,
        help="This field cannot be left blank!"
        )
    parser.add_argument(
        'amount',
        type= float,
        required=True,
        help="This field cannot be left blank!"
        )

    @jwt_required()
    def post(self):
        data = Top__up.parser.parse_args()
        user = User.find_by_account_number(data['account_number'])
        #user.money_in_the_bag = float(user.money_in_the_bag)
        if user:
            settlement = Settlement_to.find_by_account_number(235522)
            if settlement:
                print ("")
            else:
                settlement = Settlement_to("235522","9999999999999")

            user.account_balance = float(user.account_balance)
            print (settlement.account_number)
            settlement.account_balance = float(settlement.account_balance)
            settlement.account_balance = settlement.account_balance - data['amount']
            user.account_balance = data['amount'] + user.account_balance
            user.account_balance =str(user.account_balance)
            settlement.account_balance =str(settlement.account_balance)

            list=random.sample(range(9999999), 1)
            number = random.choice(list)

            transaction = Transaction(
                        number,
                        "money added to users account from settlement",
                        "credit",
                        "account top up",
                        "pending",
                        data['account_number'],
                        "235522",
                        data['amount']
                            )
            try:
                User.save_to_db(user)
                transaction.transaction_status = "succesful"
                Transaction.save_to_db(transaction)
            except:
                transaction.transaction_status = "Failed"
                Transaction.save_to_db(transaction)



            balance = {'transaction_id': transaction.id , 'account_balance': user.account_balance}
            response = returnfunc(True,balance,'your ubeus account has been credited')
            return response,200
        response = returnfunc(False,None,'user not found')
        return response,404



class transfer(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'account_number',
        type=str,
        required=True,
        help="This field cannot be left blank!"
        )
    parser.add_argument(
        'destination_account',
        type=str,
        required=True,
        help="This field cannot be left blank!"
        )
    parser.add_argument(
        'pin',
        type=str,
        required=True,
        help="This field cannot be left blank!"
        )
    parser.add_argument(
        'amount',
        type= float,
        required=True,
        help="This field cannot be left blank!"
        )
    parser.add_argument(
        'description',
        type= str,
        required=True,
        help="This field cannot be left blank!"
        )
    parser.add_argument(
        'transaction_type',
        type= str,
        required=True,
        help="This field cannot be left blank!"
        )

    @jwt_required()
    def post(self):

        data = transfer.parser.parse_args()
        user = User.find_by_account_number(data['account_number'])
        destination = User.find_by_account_number(data['destination_account'])

        if user is not None and destination is not None:
            user.account_balance = float(user.account_balance)
            destination.account_balance = float(destination.account_balance)

            if user.account_balance < data['amount']:
                response = returnfunc(False,None,'your account balance is less than required amount')
                return response,404

            destination.account_balance = data['amount'] + destination.account_balance
            user.account_balance = user.account_balance - data['amount']
            user.account_balance = str(user.account_balance)
            destination.account_balance = str(destination.account_balance)
            

            list=random.sample(range(9999999), 1)
            number = random.choice(list)
            transaction = Transaction(
                        number,
                        data['description'],
                        "credit",
                        data['transaction_type'],
                        "pending",
                        data['destination_account'],
                        data['account_number'],
                        data['amount']
                            )
            print (fees_account.account_balance)
            account = {'transaction_id': transaction.id , 'account_balance': user.account_balance}
            try:
                User.save_to_db(user)
                User.save_to_db(destination)
                Fee.save_to_db(fees_account)
                transaction.transaction_status = "succesful"
                Transaction.save_to_db(transaction)
            except:
                transaction.transaction_status = "Failed"
                Transaction.save_to_db(transaction)

            response = returnfunc(True,account,'you have succesfully made your transfer')
            return response,200
        response = returnfunc(False,None,'either your account or the destination account doesnt exist')
        return response,404



class lookup(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
            'transaction_id',
            type=int,
            required=True,
            help="This field cannot be left blank!"
                        )
    @jwt_required()
    def post(self):
        data = lookup.parser.parse_args()
        transaction = Transaction.find_by_id(data['transaction_id'])
        if transaction:
            response = returnfunc(True,transaction.json(),'this is your transaction info')
            return response,200
        response = returnfunc(False,None,'transaction was never made')
        return response,404



class TransferHistory(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        'account_number',
        type=str,
        required=True,
        help="This field cannot be left blank!"
                    )

    @jwt_required()
    def post(self):
        data = TransferHistory.parser.parse_args()
        user = User.find_by_account_number(data['account_number'])

        if user:
            response = returnfunc(
                        True,
                        list(map(lambda x: x.json(), Transaction.query.filter_by(source_account=user.account_number).all() + Transaction.query.filter_by(destination_account=user.account_number).all())),
                        'these are all transactions made by this user'
                        )
            return response,200

        response = returnfunc(False,None,'user was not found')
        return response,404
