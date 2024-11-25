from flask import Blueprint, jsonify
from app import db
from models import Fines, Loans
from datetime import datetime

fines_bp = Blueprint('fines', __name__)

# Get all fines
@fines_bp.route('/', methods=['GET'])
def get_fines():
    fines = Fines.query.all()
    return jsonify([{
        "id": fine.id,
        "loan_id": fine.loan_id,
        "amount": fine.amount,
        "status": fine.status
    } for fine in fines])

# Calculate and apply overdue fines
@fines_bp.route('/calculate', methods=['POST'])
def calculate_fines():
    overdue_loans = Loans.query.filter(
        Loans.due_date < datetime.now(),
        Loans.return_date == None
    ).all()
    
    for loan in overdue_loans:
        # Check if a fine already exists for this loan
        existing_fine = Fines.query.filter_by(loan_id=loan.id).first()
        if not existing_fine:
            # Calculate fine (e.g., $5 per overdue day)
            overdue_days = (datetime.now() - loan.due_date).days
            fine_amount = overdue_days * 5
            new_fine = Fines(
                loan_id=loan.id,
                amount=fine_amount,
                status='Unpaid'
            )
            db.session.add(new_fine)
    
    db.session.commit()
    return jsonify({"message": "Fines calculated successfully!"}), 200

# Update
