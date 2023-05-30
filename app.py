import json
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from modal import Customer, db, app, Book

CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show-books')
def showBooks():
    books_list = [book.to_dict() for book in Book.query.all()]
    json_data = json.dumps(books_list)
    return json_data

@app.route('/show-customers')
def showCustomers():
    customers_list = [customer.to_dict() for customer in Customer.query.all()]
    json_data = json.dumps(customers_list)
    return json_data



@app.route('/newCustomer', methods = ['POST'])
def newCostumer():
    request_data = request.get_json()
    name = request_data["name"]
    city = request_data["city"]
    age = request_data["age"]
    mail = request_data["mail"]
 
    newCustomer= Customer(name=name, city=city, age=age, mail=mail)
    db.session.add (newCustomer)
    db.session.commit()
    return "a new rcord was create"

@app.route('/updateCustomer/<id>', methods = ['POST'])
@app.route('/updateCustomer', methods=['POST'])
def updateCostumer():
    request_data = request.get_json()
    id = request_data["id"]
    name = request_data["name"]
    city = request_data["city"]
    age = request_data["age"]
    mail = request_data["mail"]

    myCustomer = db.session.query(Customer).filter_by(id=id).first()

    # myCustomer = Customer(id=id,name=name, city=city, age=age, mail=mail)
    myCustomer.name = name
    myCustomer.city = city
    myCustomer.age = age
    myCustomer.mail = mail

    # db.session.update(myCustomer)
    db.session.commit()
    return "a new rcord was create"

@app.route('/addNewBook', methods = ['POST'])
def newBook():
    request_data = request.get_json()
    name = request_data["name"]
    author = request_data["author"]
    year_published = request_data["year_published"]
    book_type = request_data["book_type"]
 
    newBook= Book(name=name, author=author, year_published=year_published, book_type=book_type)

    db.session.add (newBook)
    db.session.commit()
    return "a new rcord was create"


@app.route('/updateBook/<id>', methods = ['PUT'])
@app.route('/updateBook', methods=['POST'])
def updateBook():
    request_data = request.get_json()
    id = request_data["id"]
    name = request_data["name"]
    author = request_data["author"]
    year_published = request_data["year_published"]
    book_type = request_data["book_type"]

    myBook = db.session.query(Customer).filter_by(id=id).first()

    # myCustomer = Customer(id=id,name=name, city=city, age=age, mail=mail)
    myBook.name = name
    myBook.author = author
    myBook.year_published = year_published
    myBook.book_type = book_type

    # db.session.update(myCustomer)
    db.session.commit()
    return "a new rcord was create"


@app.route('/deletecustomer/<id>', methods = ['DELETE'])
@app.route('/deletecustomer/', methods = ['DELETE'])
def deleteCustomer(id=-1):
    del_row = Customer.query.filter_by(id=id).first()
    if del_row:
        db.session.delete(del_row)
        db.session.commit()
        return "a row was delete"
    return "no such customer...."    



@app.route('/deletebook/<id>', methods = ['DELETE'])
@app.route('/deletebook/', methods = ['DELETE'])
def deleteBook(id=-1):
    del_row = Book.query.filter_by(id=id).first()
    if del_row:
        db.session.delete(del_row)
        db.session.commit()
        return "a row was delete"
    return "no such book...."    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)