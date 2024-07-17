from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from dotenv import dotenv_values
import requests

books_bp = Blueprint('books', __name__)
API_KEY = dotenv_values(".env").get("API_KEY")


@books_bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template('home.html', user=current_user)


@books_bp.route('/book/<isbn>', methods=['GET', 'POST'])
def book(isbn):
    if request.method == 'GET':
        req = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={API_KEY}'
        response = requests.get(req)
        response.raise_for_status()
        book_data = response.json()

        if 'items' not in book_data:
            return jsonify({'error': 'No book found.'}), 404


@books_bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        isbn_code = request.form['isbnInput']
        req = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn_code}&key={API_KEY}'
        response = requests.get(req)
        response.raise_for_status()
        book_data = response.json()
        print(book_data)
        
    return render_template('search.html', user=current_user)
