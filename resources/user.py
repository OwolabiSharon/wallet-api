import random
from db import db
from models.user import *
from flask_restful import Resource, reqparse, inputs
from flask_jwt_extended import create_access_token,jwt_required


# all endpoint responses are to be called from a function or from a dictionary key value pair thingy
#ill do it later😁

def plausibleAccNo():
    number = random.sample(range(999999999), 1)



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
            return {
                'status':False,
                'message':'user exists'
            },400
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
        return {
            'status': True,
            'data':user.json(),
            'message':'user created succesfully'
        },201


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
            return {
            'status': True,
            'data': access_token,
            'message':'you are logged in'
                   },200
        return {
            'status':False,
            'message':'user not found'
                },404



class Account_balance(Resource):
    @jwt_required()
    def get(self, account_number):
        user = User.find_by_account_number(account_number)
        balance = user.account_balance
        #user =user.phone_number[x.json() for x in Received_Transfer.query.all()]
        if user:
            return {
                'status':True,
                'data': balance,
                'message':'this is your account balance'
                        }

        return {
            'status':True,
            'user': 'does not exist'
                },404


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
    def put(self):
        data = Top__up.parser.parse_args()
        user = User.find_by_account_number(data['account_number'])
        #user.money_in_the_bag = float(user.money_in_the_bag)
        if user:
            user.account_balance = float(user.account_balance)
            user.account_balance = data['ammount'] + user.account_balance
            user.account_balance =str(user.account_balance)

            User.save_to_db(user)
            json = user.account_balance
            return{
            'status':True,
            'data': json,
            'message':'your ubeus account has been credited'
                        },200
        return{
        'status': False,
        'message':'user does not exist'
                },404


class Transfer(Resource):
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

        data = Transfer.parser.parse_args()
        user = User.find_by_account_number(data['account_number'])
        destination = User.find_by_account_number(data['destination_account'])

        if user is not None and destination is not None:
            user.account_balance = float(user.account_balance)
            destination.account_balance = float(destination.account_balance)

            if user.account_balance < data['amount']:
                return {'message':'your account balance is less than required amount'}

            destination.account_balance = data['amount'] + destination.account_balance
            user.account_balance = user.account_balance - data['amount']
            user.account_balance = str(user.account_balance)
            destination.account_balance = str(destination.account_balance)

            fees_account = Fee('00000' , '00')
            fees_account.account_balance = float(fee_account.account_balance)
            fees_account.account_balance = fee_account.account_balance + data['amount'] / 100
            fees_account.account_balance = str(fee_account.account_balance)

            transaction = Transfer(
                        data['description'],
                        "credit",
                        data['transaction_type'],
                        "pending",
                        data['destination_account'],
                        data['source_account'],
                        data['amount']
                            )

            Transaction.save_to_db(transaction)
            User.save_to_db(user)
            User.save_to_db(destination)
            Fee.save_to_db(fees_account)

            account = user.account_balance
            return {
                'status':True,
                'data': account,
                'message':'you have succesfully made your transfer'
                   }
        return {
            'status':False,
            'data': "",
            'message':'either your account or the destination account doesnt exist'
               }
