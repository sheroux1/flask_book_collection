from lib2to3.pgen2 import token
from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/test')
def testData():
    return {'This': 'Test'}

@api.route('/book', methods = ['GET'])
@token_required
def get_books(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    response = books_schema.dump(books)
    return jsonify(response)

@api.route('/book', methods = ['POST'])
@token_required
def create_book(current_user_token):
    isbn = request.json['isbn']
    title = request.json['title']
    author_first = request.json['author_first']
    author_last = request.json['author_last']
    book_length = request.json['book_length']
    is_fiction = request.json['is_fiction']
    user_token = current_user_token.token

    print(f'Just a test: {current_user_token.token}')

    book = Book(isbn, title, author_first, author_last, book_length, is_fiction, user_token = user_token)

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

@api.route('book/<book_id>', methods = ['GET'])
@token_required
def get_single_car(current_user_token, book_id):
    book = Book.query.get(book_id)
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('book/<book_id>', methods = ['POST', 'PUT'])
@token_required
def update_book(current_user_token, book_id):
    book = Book.query.get(book_id)
    book.isbn = request.json['isbn']
    book.title = request.json['title']
    book.author_first = request.json['author_first']
    book.author_last = request.json['author_last']
    book.book_length = request.json['book_length']
    book.is_fiction = request.json['is_fiction']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('book/<book_id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)

@api.route('book/<book_id>', methods = ['GET'])
@token_required
def get_single_book(current_user_token, book_id):
    book = Book.query.get(book_id)
    response = book_schema.dump(book)
    return jsonify(response)