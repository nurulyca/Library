from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
import jwt

app = Flask(__name__)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres@localhost:5432/excer'


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(28), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True, index=True)
    stock = db.Column(db.Integer, index=True)
    title = db.Column(db.String(100), index=True)
    author = db.Column(db.String(100), nullable=False)

class Transactions(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, foreign_key=True, index=True)
    book_id = db.Column(db.Integer, foreign_key=True, index=True)
    checkout_date = db.Column(db.String, nullable=False)
    return_date = db.Column(db.String, nullable=True)


#endpoints of user
@app.route('/users/')
def get_users():
    return jsonify([
        {
            'user_id': user.user_id, 
            'name': user.name, 
            'email': user.email, 
            'password' : user.password
            } for user in Users.query.all()
    ]) 

@app.route('/users/<id>/')
def get_user(id):
    user = Users.query.filter_by(user_id=id).first_or_404()
    return {
            'user_id': user.user_id, 
            'name': user.name, 
            'email': user.email, 
            'password' : user.password
        } 

#register of users
@app.route('/register_users/', methods=['POST'])
def create_user():
    data = request.get_json()
    if not 'name' in data and not 'email' in data and not 'password' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Name or email or password not given'
        }), 400
    if len(data['name']) < 4 or len(data['email']) < 6:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Name and email must contain minimum of 4 letters'
        }), 400
    
    pw_hash = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
    u = Users(
            name=data['name'],
            username=data['username'],
            email=data['email'],
            password=pw_hash
        )
    db.session.add(u)
    db.session.commit() 
    return{ 
        'user_id': u.user_id, 
        'name': u.name, 
        'username' : u.username,
        'email': u.email, 
        'password' : u.password
    }, 201

#login of users
@app.route('/login_users/', methods = ['POST'])
def login_users():
    data = request.get_json()
    if not 'email' in data and not 'password' in data:
        return jsonify({
            'error' : 'Bad Request',
            'message' : 'Email or password must be given'
        }), 400

    user = Users.query.filter_by(email = data["email"]).first_or_404()

    payload = {'user_id': user.user_id, 'email': user.email}

    encoded_jwt = jwt.encode(payload, "secret", algorithm="HS256")

    if bcrypt.check_password_hash(user.password, data["password"]):
        return jsonify ({
            'user_id': user.user_id, 
            'name': user.name, 
            'email': user.email, 
            'password' : user.password,
            'access_token': encoded_jwt.decode('utf-8') #bytes
        })
    else:
        return jsonify ({
            'message' : 'Wrong password!'
        })

@app.route('/users/<id>/', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = Users.query.filter_by(user_id=id).first_or_404()
    if 'password'in data:
        users.password=data['password']
    if 'email' in data:
        users.email = data['email']
    if 'name' in data:
        users.name = data['name']
    
    db.session.commit()
    return jsonify({
            'user_id': users.user_id, 
            'name': users.name, 
            'email': users.email, 
            'password' : users.password
        })

@app.route('/users/<id>/', methods=['DELETE'])
def delete_user(id):
    user = Users.query.filter_by(user_id=id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return {
        'success': 'User deleted successfully'
    }

#endpoints of book
@app.route('/book/')
def get_books():
    return jsonify([
        {   'book_id': book.book_id, 
            'stock' : book.stock,
            'title': book.title, 
            'author': book.author
        } for book in Book.query.all()
    ])

@app.route('/book/<id>')
def get_book(id):
    book = Book.query.filter_by(book_id=id).first_or_404()
    return jsonify({
            'book_id': book.book_id, 
            'stock' : book.stock,
            'title': book.title, 
            'author': book.author
    })

@app.route('/book/', methods=['POST'])
def create_book():
    data = request.get_json()
    if not 'title' in data or not 'author' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Title or author not given'
        }), 400
    if len(data['title']) < 1:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Title of book should contain minimum of 1 letter'
        }), 400
    book = Book(
        title = data["title"], 
        author = data["author"]
    )
    db.session.add(book)
    db.session.commit()
    return {
            'book_id': book.book_id, 
            'stock' : book.stock,
            'title': book.title, 
            'author': book.author
    }, 201

@app.route('/book/<id>/', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    book = Book.query.filter_by(book_id=id).first_or_404()

    if 'author'in data:
        book.author = data['author']
    if 'title' in data:
        book.title = data['title']
    if 'stock' in data:
        book.title = data['stock']

    db.session.commit()
    return {
            'book_id': book.book_id, 
            'stock' : book.stock,
            'title': book.title, 
            'author': book.author
    }, 201

@app.route('/book/<id>/', methods=['DELETE'])
def delete_book(id):
    book = Book.query.filter_by(book_id=id).first_or_404()
    db.session.delete(book)
    db.session.commit()
    return {
        'success': 'Book deleted successfully'
    }

#endpoints of Transaction
@app.route('/transaction/')
def get_transaction():
    return jsonify([
        {
            'transaction_id': transaction.transaction_id, 
            'user_id': transaction.user_id, 
            'book_id': transaction.book_id, 
            'checkout_date': transaction.checkout_date, 
            'return_date': transaction.return_date
        } for transaction in Transactions.query.all()
    ])

@app.route('/transaction/<id>')
def get_transactions(id):
    transaction = Transactions.query.filter_by(transaction_id=id).first_or_404()
    return jsonify({
            'transaction_id': transaction.transaction_id, 
            'user_id': transaction.user_id, 
            'book_id': transaction.book_id, 
            'checkout_date': transaction.checkout_date, 
            'return_date': transaction.return_date
    })

#listing books which one user has been borrowed
@app.route('/transaction/user/<id>')
def get_user_transaction(id):
    transaction = Transactions.query.filter_by(user_id=id)
    return jsonify([
        {   'transaction_id': transaction.transaction_id, 
            'user_id': transaction.user_id, 
            'book_id': transaction.book_id, 
            'checkout_date': transaction.checkout_date, 
            'return_date': transaction.return_date
        } for transaction in transaction
    ])

#create a transaction
@app.route('/transaction/', methods=['POST'])
def create_transaction():
    data = request.get_json()
    if not 'user_id' in data and not 'book_id' in data and not 'checkout_date' in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'User ID or book ID or check out date not given'
        }), 400

    token = request.headers.get("access_token").encode('utf-8') 

    try:
        decoded_token = jwt.decode(token, 'secret', algorithm=["HS256"])
    except jwt.exceptions.DecodeError:
        return "Access token is invalid!"

    if not 'user_id' in decoded_token and not 'email' in decoded_token:
        return jsonify({
            'error' : 'Bad Request',
            'message' : 'Access token is invalid!'
        }), 400

    bookSelected = Book.query.filter_by(book_id = data['book_id']).first_or_404()
    listTransaction = Transactions.query.filter_by(book_id=data['book_id'], return_date=None).count()

    if bookSelected.stock <= listTransaction:
        return jsonify({
            'error' : 'Book is out of stock'
        }), 400

    transaction = Transactions(
        user_id = decoded_token['user_id'], 
        book_id = data["book_id"], 
        checkout_date = data["checkout_date"]
    )
    
    db.session.add(transaction)
    db.session.commit()
    return {
            'transaction_id': transaction.transaction_id, 
            'user_id': transaction.user_id, 
            'book_id': transaction.book_id, 
            'checkout_date': transaction.checkout_date, 
            'return_date': transaction.return_date, 
            'in_stock' : bookSelected.stock - listTransaction - 1
    }, 201

@app.route('/transaction/<id>/', methods=['PUT'])
def update_transaction(id):
    data = request.get_json()
    transaction = Transactions.query.filter_by(transaction_id=id).first_or_404()

    if 'user_id'in data:
        transaction.user_id = data['user_id']
    if 'book_id' in data:
        transaction.book_id = data['book_id']
    if 'checkout_date' in data:
        transaction.checkout_date = data["checkout_date"]

    db.session.commit()
    return {
            'transaction_id': transaction.transaction_id, 
            'user_id': transaction.user_id, 
            'book_id': transaction.book_id, 
            'checkout_date': transaction.checkout_date, 
            'return_date': transaction.return_date
    }, 201

#return book
@app.route('/return_book/<id>/', methods = ['PUT'])
def return_transaction(id):
    data = request.get_json()
    transaction = Transactions.query.filter_by(transaction_id=id).first_or_404()

    token = request.headers.get("access_token").encode('utf-8')

    try:
        decoded_token = jwt.decode(token, 'secret', algorithm=["HS256"])
    except jwt.exceptions.DecodeError:
        return "Access token is invalid!"
    
    if not 'user_id' in decoded_token and not 'email' in decoded_token and not 'password' in decoded_token:
        return jsonify({
            'error' : 'Bad Request',
            'message' : 'Access token is invalid!'
        }), 400
    if decoded_token['user_id'] != transaction.user_id:
        return jsonify ({
            'error' : 'Bad Request',
            'message' : 'Access token is invalid!'
        }), 400

    if not 'return_date' in data:
        return jsonify({
            'error' : 'Bad Request',
            'message' : 'Return date not given'
        }), 400

    if 'return_date' in data:
        transaction.return_date = data["return_date"]
    db.session.commit()
    return {
            'transaction_id': transaction.transaction_id, 
            'user_id': transaction.user_id, 
            'book_id': transaction.book_id, 
            'checkout_date': transaction.checkout_date, 
            'return_date': transaction.return_date
    }, 201

@app.route('/transaction/<id>/', methods=['DELETE'])
def delete_transaction(id):
    transaction = Transactions.query.filter_by(transaction_id=id).first_or_404()
    db.session.delete(transaction)
    db.session.commit()
    return {
        'success': 'Transaction deleted successfully'
    }

if __name__ == '__main__':
    app.run(debug=True)