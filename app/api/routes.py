from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'totally': 'tubular'}


@api.route('/library', methods = ['POST'])
@token_required
def add_book(current_user_token):
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    book_title = request.json['book_title']
    book_length = request.json['book_length']
    book_type = request.json['book_type']
    language = request.json['language']
    isbn = request.json['isbn']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(first_name, last_name, book_title, book_length, book_type, language, isbn, user_token = user_token )

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)


# GET method to retrieve data that has been created

@api.route('/library', methods = ['GET'])
@token_required
def get_books(current_user_token):
    a_user = current_user_token.token
    contacts = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(contacts)
    return jsonify(response)



# GET method to call a specific contact with an ID number

@api.route('/library/<id>', methods = ['GET'])
@token_required
def get_single_book(current_user_token, id):
    single_contact = Book.query.get(id)
    response = book_schema.dump(single_contact)
    return jsonify(response)


# UPDATE endpoint
@api.route('/library/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,id):
    book = Book.query.get(id) 
    book.first_name = request.json['first_name']
    book.last_name = request.json['last_name']
    book.book_title = request.json['book_title']
    book.book_length = request.json['book_length']
    book.book_type = request.json['book_type']
    book.language = request.json['language']
    book.isbn = request.json['isbn']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)


# DELETE car ENDPOINT
@api.route('/library/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)