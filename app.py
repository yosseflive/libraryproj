import json
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from modal import Customer, db, app, Book

CORS(app)

@app.route('/')
def index():
    return ("""
<!DOCTYPE html>
<html lang="en">

<head>
    <title>library</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    <style>
        /* Remove the navbar's default margin-bottom and rounded borders */
        .navbar {
            margin-bottom: 0;
            border-radius: 0;
        }

        /* Set height of the grid so .sidenav can be 100% (adjust as needed) */
        .row.content {
            height: 450px
        }

        /* Set gray background color and 100% height */
        .sidenav {
            padding-top: 20px;
            background-color: #f1f1f1;
            height: 100%;
        }

        /* Set black background color, white text and some padding */
        footer {
            background-color: #555;
            color: white;
            padding: 15px;
        }

        /* On small screens, set height to 'auto' for sidenav and grid */
        @media screen and (max-width: 767px) {
            .sidenav {
                height: auto;
                padding: 15px;
            }

            .row.content {
                height: auto;
            }
        }
    </style>
</head>

<body>

    <nav class="navbar navbar-inverse">
        <div class="container-fluid">
            <div class="navbar-header">
                <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                </button>
                <a class="navbar-brand" href="#">CRM</a>
            </div>
            <div class="collapse navbar-collapse" id="myNavbar">
                <ul class="nav navbar-nav">
                    <li class="active"><a href="home.html" target="main">Home</a></li>
                    <li><a href="books.html" target="main">Books</a></li>
                    <li><a href="customers.html" target="main">Customers</a></li>
                    <li><a href="loans.html" target="main">Loan</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container-fluid text-center">
        <div class="row content">
            <div class="col-sm-2 sidenav">
                <p><a href="addBooks.html" target="main" id="main">add new Books</a></p>
                <p><a href="addCustomers.html" target="main" id="main">add new Customers</a></p>
                <p><a href="updateCustomer.html" target="main" id="updatecustomerid">update Customer</a></p>
                <p><a href="updateBook.html" target="main" id="updatebookid">update Book</a></p>
                <p><a href="loans.html" target="main" id="main">Loan</a></p>
            </div>
            <div class="col-sm-8 text-left">
                <iframe src="home.html" name="main" style="height: 49dvh; width: 60dvw;"></iframe>
            </div>
            <div class="col-sm-2 sidenav">
                <div class="well">
                    <p>ADS</p>
                </div>
                <div class="well">
                    <p>ADS</p>
                </div>
            </div>
        </div>
    </div>

    <footer class="container-fluid text-center">
        <p>Footer Text</p>
    </footer>

</body>

</html>""")

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