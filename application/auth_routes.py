from main import app
from flask import render_template, request, redirect, url_for, flash, session
# from flask_login import LoginManager, current_user, login_required, logout_user, login_user
from application.database import db
from application.models import Role, User

@app.route("/first_page_registration", methods=['GET', 'POST']) # type: ignore
def first_page_registration():
    if request.method == "GET":
        return render_template('first_page_registration.html')
    
    if request.method == "POST":
        role = request.form.get('role')
        if not request.form.get('role'):
            flash('Please select a role')
            return redirect(url_for('first_page_registration'))
        
        session['role'] = role
        return redirect(url_for('register'))
    
    
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        return render_template('register.html')
    
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        role = session.get('role')
        
    # Do some validation
    if len(password)<6:
        flash('Password must be at least 6 characters')
        return redirect(url_for('register'))
    
    if len(username)<3 or not username.isalnum():
        flash('Username must be at least 3 characters and alphanumeric')
        return redirect(url_for('register'))
    
    if len(email)<5 or not '@' in email or not '.' in email:
        flash('Invalid email, please enter a valid email address, e.g. abc@gmail.com')
        return redirect(url_for('register'))
    
    if password != confirm_password:
        flash('Passwords do not match, please try again')
        return redirect(url_for('register'))
    
    # if not role:
    #     flash('Please select a role')
    #     return redirect(url_for('register'))
    
    if User.query.filter_by(username=username).first():
        flash('Username already exists')
        return redirect(url_for('register'))
    
    if User.query.filter_by(email=email).first():
        flash('Email already exists')
        return redirect(url_for('register'))
    
    if not username or not email or not password:
        flash('Please fill all fields')
        return redirect(url_for('register'))
    
    try:    
        user = User(username=username, email=email, password=password, role = role,  
                    roles=[Role.query.filter_by(role_name=role).first()])
        db.session.add(user)
        db.session.commit()
        flash('User created successfully')
        return redirect(url_for('login'))
    except Exception as e:
        flash('An error occurred')
        return redirect(url_for('register'))
    

@app.route('/login', methods = ['GET', 'POST']) # type: ignore
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Please fill all fields')
            return redirect(url_for('login'))
        
        user = User.query.filter_by(username=username).first()
        
        if not user:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        if user.password != password:
            flash('Invalid username or password')
            return redirect(url_for('login'))

        session['user_id'] = user.id
        session['username'] = user.username
        session['email'] = user.email
        session['role'] = user.roles[0].role_name

        flash('Login successful')
        return redirect(url_for('all_campaign'))

@app.route('/forgot_password', methods=['GET','POST']) # type: ignore
def forgot_password():
    if request.method == 'GET':
        return render_template('forgot_password.html')
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Email not found')
            return redirect(url_for('forgot_password'))
        
        flash('An email has been sent to you with instructions on how to reset your password')
        return redirect(url_for('login'))
    

@app.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('index'))

