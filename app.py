from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from db import *
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import re
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-unique-and-secret-key'

init_db(app)

projects = [{
    'title': 'project 1',
    'date': '24/03/2005 - 10:55',
    'description': 'aaaa '*200,
    'creator': 'You'
}] * 10

@app.route('/')
def home():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.get(user_id)
    else:
        user = None
    return render_template('index.html', user=user , projects=projects)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('pswd')

        print(f"Email: {email}, Password: {password}")

        # Check if the email and password are provided
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400

        # Look for the user in the database by email
        user = db.session.query(User).filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            # If the user is found and the password is correct, log the user in
            session['user_id'] = user.ID
            # Ensure it redirects with GET method to the home route
            return jsonify({'message': 'loged in succefully'}), 200  # Flask automatically uses GET method for redirects
        else:
            return jsonify({'error': 'Invalid email or password'}), 401



@app.route('/createaccount', methods=['POST'])
def create_account():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    cpassword = data.get('cpassword')
    
    if not username or not email or not password or not cpassword:
        return jsonify({'error': 'All fields are required'}), 400
    
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters long'}), 400
    
    if not re.match(r'^[a-zA-Z0-9_.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return jsonify({'error': 'Invalid email format'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400
    
    if password != cpassword:
        return jsonify({'error': 'Passwords do not match'}), 400
    
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({'error': 'Username or email already taken'}), 400
    
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    #log the user in
    session['user_id'] = new_user.ID

    return jsonify({'message': 'Account created successfully'}), 201

@app.route('/logout')
def logout():
    if 'user_id' not in session:
        return "<h1>you are not loged in</h1>"
    else:
        session.clear()
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
