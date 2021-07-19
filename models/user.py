from db import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(11))
    firstname = db.Column(db.String(80))
    middlename = db.Column(db.String(80))
    lastname = db.Column(db.String(80))
    date_of_birth = db.Column(db.String(60))
    password = db.Column(db.String(80))
    account_balance = db.Column(db.String(800))
    email = db.Column(db.String(80))
    pin = db.Column(db.String(400))



    def __init__(self, account_number,firstname,middlename,lastname,date_of_birth, password,email,pin, account_balance):
        self.account_number = account_number
        self.firstname = firstname
        self.middlename = middlename
        self.lastname = lastname
        self.date_of_birth = date_of_birth
        self.password = password
        self.email = email
        self.pin = pin
        self.account_balance = account_balance


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'account_number':self.account_number,
            'firstname':self.firstname,
            'middlename':self.middlename,
            'lastname':self.lastname,
            'date_of_birth':self.date_of_birth,
            'password':self.password,
            'email':self.email,
            'pin':self.pin,
            'account_balance':self.account_balance
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_password(cls, password):
        return cls.query.filter_by(password=password).first()

    @classmethod
    def find_by_pin(cls, pin):
        return cls.query.filter_by(pin=pin).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()


class Transaction(db.Model):
    __TableName__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(900))
    transaction_direction = db.Column(db.String(900))
    transaction_type = db.Column(db.String(800))
    transaction_status = db.Column(db.String(10))
    destination_account = db.Column(db.String(800))
    source_account = db.Column(db.String(80))
    amount = db.Column(db.String(800))


    def __init__(self,description,transaction_direction,transaction_type,transaction_status,destination_account,source_account,amount,user_id):

        self.description = description
        self.transaction_direction = transaction_direction
        self.transaction_type = transaction_type
        self.transaction_status = transaction_status
        self.destination_account = destination_account
        self.source_account = source_account
        self.amount = amount

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'description':self.description,
            'transaction_direction':self.transaction_direction,
            'transaction_type':self.transaction_type,
            'transaction_status':self.transaction_status,
            'destination_account':self.destination_account,
            'source_account':self.source_account,
            'amount':self.amount
        }



class Settlement_to(db.Model):
    __tablename__ = 'settlement_to'

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(11))
    account_balance = db.Column(db.String(800))



    def __init__(self, account_number,account_balance):
        self.account_number = account_number
        self.account_balance = 9999999999999


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_password(cls, password):
        return cls.query.filter_by(password=password).first()


class Settlement_fro(db.Model):
    __tablename__ = 'settlement_fro'

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(11))
    account_balance = db.Column(db.String(800))



    def __init__(self, account_number,account_balance):
        self.account_number = account_number
        self.account_balance = 0000000000000


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_password(cls, password):
        return cls.query.filter_by(password=password).first()


class Fee(db.Model):
    __tablename__ = 'fees'

    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String(11))
    account_balance = db.Column(db.String(800))



    def __init__(self, account_number,account_balance):
        self.account_number = account_number
        self.account_balance = account_balance


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_password(cls, password):
        return cls.query.filter_by(password=password).first()
