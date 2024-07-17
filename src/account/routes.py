from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from src import db
from flask_login import login_user, logout_user, login_required, current_user

account_bp = Blueprint('account', __name__)


@account_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user:
            if user.check_password(password):
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
