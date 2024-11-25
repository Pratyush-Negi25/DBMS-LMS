from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Import models
from models import Books, Members, Loans, Fines

@app.route('/')
def index():
    return render_template('index.html')

# Books Management
@app.route('/books', methods=['GET', 'POST'])
def manage_books():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        genre = request.form['genre']
        quantity = request.form['quantity']
        new_book = Books(title=title, author=author, isbn=isbn, genre=genre, quantity=quantity)
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!')
    books = Books.query.all()
    return render_template('books.html', books=books)

# Members Management
@app.route('/members', methods=['GET', 'POST'])
def manage_members():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        membership_start = datetime.now()
        membership_end = membership_start + timedelta(days=365)
        new_member = Members(name=name, email=email, phone=phone, membership_start=membership_start, membership_end=membership_end)
        db.session.add(new_member)
        db.session.commit()
        flash('Member registered successfully!')
    members = Members.query.all()
    return render_template('members.html', members=members)

# Loans Management
@app.route('/loans', methods=['GET', 'POST'])
def manage_loans():
    if request.method == 'POST':
        book_id = request.form['book_id']
        member_id = request.form['member_id']
        due_date = datetime.now() + timedelta(days=14)
        new_loan = Loans(book_id=book_id, member_id=member_id, due_date=due_date)
        db.session.add(new_loan)
        db.session.commit()
        flash('Book loaned successfully!')
    loans = Loans.query.all()
    books = Books.query.all()
    members = Members.query.all()
    return render_template('loans.html', loans=loans, books=books, members=members)

# Fines Management
@app.route('/fines')
def manage_fines():
    fines = Fines.query.all()
    overdue_loans = Loans.query.filter(Loans.due_date < datetime.now(), Loans.return_date == None).all()
    for loan in overdue_loans:
        existing_fine = Fines.query.filter_by(loan_id=loan.id).first()
        if not existing_fine:
            overdue_days = (datetime.now() - loan.due_date).days
            fine_amount = overdue_days * 5  # Assuming $5 per day
            new_fine = Fines(loan_id=loan.id, amount=fine_amount, status='Unpaid')
            db.session.add(new_fine)
            db.session.commit()
    return render_template('fines.html', fines=fines)

if __name__ == '__main__':
    app.run(debug=True)
