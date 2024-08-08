from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from src import db
from werkzeug.security import generate_password_hash, check_password_hash


account_bp = Blueprint('account', __name__)


@account_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return redirect(url_for('books.home'))
            else:
                flash('Incorrect password', category='danger')
        else:
            flash('User does not exist', category='danger')
    return render_template('login.html', user=current_user)


@account_bp.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('account.login'))


@account_bp.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        if password1 == password2:
            new_user = User(username=username, password=generate_password_hash(password1))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('account.login'))
        else:
            flash('Passwords do not match', category='danger')
    return render_template('sign_up.html', user=current_user)
