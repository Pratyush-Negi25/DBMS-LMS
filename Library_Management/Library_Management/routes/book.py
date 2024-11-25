from flask import Blueprint, request, jsonify
from app import db
from models import Books

books_bp = Blueprint('books', __name__)

@books_bp.route('/', methods=['GET'])
def get_books():
    books = Books.query.all()
    return jsonify([{
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "isbn": book.isbn,
        "genre": book.genre,
        "quantity": book.quantity
    } for book in books])

@books_bp.route('/', methods=['POST'])
def add_book():
    data = request.json
    new_book = Books(
        title=data['title'],
        author=data['author'],
        isbn=data['isbn'],
        genre=data['genre'],
        quantity=data['quantity']
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added successfully!"}), 201
