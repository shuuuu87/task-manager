from flask import Blueprint, render_template, redirect, url_for, flash, request, session, Response
from app.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from app.forms import RegisterForm, LoginForm
from flask_migrate import upgrade  # for running db upgrade

auth_bp = Blueprint('auth', __name__)

# Register route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email is already registered.', 'danger')
            return redirect(url_for('auth.register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

# Login route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user, remember=True)
            session['user_id'] = user.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home.homepage'))
        else:
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login'))

    return render_template('login.html', form=form)

# Logout route
@auth_bp.route('/logout')
def logout():
    logout_user()
    session.pop('user_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('auth.login'))

# TEMP route to run migration upgrade on Render
@auth_bp.route('/run-db-upgrade')
def run_db_upgrade():
    try:
        upgrade()
        return Response("Database upgraded successfully!", mimetype='text/plain')
    except Exception as e:
        return Response(f"Error: {e}", mimetype='text/plain')
