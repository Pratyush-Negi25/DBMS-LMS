from flask import Blueprint, request, jsonify
from app import db
from models import Loans, Books, Members
from datetime import datetime, timedelta

loans_bp = Blueprint('loans', __name__)

# Get all loans
@loans_bp.route('/', methods=['GET'])
def get_loans():
    loans = Loans.query.all()
    return jsonify([{
        "id": loan.id,
        "book_id": loan.book_id,
        "member_id": loan.member_id,
        "borrow_date": loan.borrow_date,
        "due_date": loan.due_date,
        "return_date": loan.return_date
    } for loan in loans])

# Add a new loan (borrow a book)
@loans_bp.route('/', methods=['POST'])
def add_loan():
    data = request.json
    book_id = data['book_id']
    member_id = data['member_id']
    
    # Check if the book is available
    book = Books.query.get(book_id)
    if not book or book.quantity < 1:
        return jsonify({"error": "Book not available"}), 400
    
    # Create a new loan
    due_date = datetime.now() + timedelta(days=14)
    new_loan = Loans(
        book_id=book_id,
        member_id=member_id,
        borrow_date=datetime.now(),
        due_date=due_date
    )
    db.session.add(new_loan)
    
    # Reduce book quantity
    book.quantity -= 1
    db.session.commit()
    
    return jsonify({"message": "Loan added successfully!", "due_date": due_date}), 201

# Return a book
@loans_bp.route('/<int:loan_id>/return', methods=['POST'])
def return_book(loan_id):
    loan = Loans.query.get(loan_id)
    if not loan or loan.return_date is not None:
        return jsonify({"error": "Invalid loan or book already returned"}), 400
    
    # Mark the loan as returned
    loan.return_date = datetime.now()
    
    # Increase book quantity
    book = Books.query.get(loan.book_id)
    if book:
        book.quantity += 1
    
    db.session.commit()
    return jsonify({"message": "Book returned successfully!"}), 200
