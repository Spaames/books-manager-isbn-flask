from flask import Blueprint, render_template, url_for, redirect, flash, request

account_bp = Blueprint('account', __name__)


@account_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@account_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    pass
