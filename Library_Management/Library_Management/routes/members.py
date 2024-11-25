from flask import Blueprint, request, jsonify
from app import db
from models import Members
from datetime import datetime, timedelta

members_bp = Blueprint('members', __name__)

@members_bp.route('/', methods=['GET'])
def get_members():
    members = Members.query.all()
    return jsonify([{
        "id": member.id,
        "name": member.name,
        "email": member.email,
        "phone": member.phone,
        "membership_start": member.membership_start,
        "membership_end": member.membership_end
    } for member in members])

@members_bp.route('/', methods=['POST'])
def add_member():
    data = request.json
    membership_start = datetime.now()
    membership_end = membership_start + timedelta(days=365)
    new_member = Members(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        membership_start=membership_start,
        membership_end=membership_end
    )
    db.session.add(new_member)
    db.session.commit()
    return jsonify({"message": "Member added successfully!"}), 201
