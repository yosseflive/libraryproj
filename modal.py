import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
           'sqlite:///' + os.path.join(basedir, 'library.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    age = db.Column(db.Integer)
    mail = db.Column(db.String(100))
    loans = db.relationship('Loan', backref='customer')

    def __repr__(self):
        return f"Customer: ('{self.id}','{self.name}','{self.city}','{self.age}','{self.mail}',)"
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'age': self.age,
            'mail': self.mail
        }
    
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    author = db.Column(db.String(50))
    year_published = db.Column(db.Integer)
    book_type = db.Column(db.Integer)
    loans = db.relationship('Loan', backref='book')

    def __repr__(self):
        return f"Book: ('{self.id}','{self.name}','{self.author}','{self.year_published}','{self.book_type}',)"
    

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'year_published': self.year_published,
            'book_type': self.book_type,
        }


class Loan(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    loan_date = db.Column(db.Date)
    return_date = db.Column(db.Date)

    def __repr__(self):
        return f'<Loan "{self.loan_date}"'

    def __init__(self, cust_id, book_id, loan_date, return_date):
        self.cust_id = cust_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.return_date = return_date

    def to_dict(self):
        return {
            'id': self.id,
            'cust_id': self.cust_id,
            'book_id': self.book_id,
            'loan_date': self.loan_date,
            'return_date': self.return_date
        }
