from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from dotenv import dotenv_values
import requests
from .models import Book, Status
from src import db

books_bp = Blueprint('books', __name__)
API_KEY = dotenv_values(".env").get("API_KEY")


@books_bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    reading_list = Book.query.filter_by(user_id=current_user.id, status_id=1).all()
    read_list = Book.query.filter_by(user_id=current_user.id, status_id=2).all()
    to_buy_list = Book.query.filter_by(user_id=current_user.id, status_id=3).all()
    to_read_list = Book.query.filter_by(user_id=current_user.id, status_id=4).all()
    book_list = Book.query.filter_by(user_id=current_user.id).all()

    return render_template('home.html',
                           user=current_user,
                           read_list=read_list,
                           to_buy_list=to_buy_list,
                           to_read_list=to_read_list,
                           reading_list=reading_list,
                           book_list=book_list,
                           background_color="page_book")


@books_bp.route('/search', methods=['GET', 'POST'])
def search():
    new_book = ""
    if request.method == 'POST':
        isbn_code = request.form['isbnInput']
        req = f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn_code}&key={API_KEY}'
        response = requests.get(req)
        response.raise_for_status()
        books_data = response.json()
        if 'items' not in books_data:
            return jsonify({'error': 'Aucun livre trouvé pour cet ISBN'})
        book_data = books_data['items'][0]['volumeInfo']
        print(book_data)
        title = book_data.get('title', 'N/A')
        subtitle = book_data.get('subtitle', 'N/A')
        author_list = book_data.get('authors', 'N/A')
        author = author_list[0] if author_list else 'N/A'
        description = book_data.get('description', 'N/A')
        new_book = Book(title=title,
                        subtitle=subtitle,
                        authors=author,
                        description=description,
                        status_id=0,
                        user_id=current_user.id)

    return render_template('search.html', user=current_user, book=new_book, background_color="page_book")


@books_bp.route('/save_book', methods=['GET', 'POST'])
def status():
    if request.method == 'POST':
        if request.form['statusList'] != 0:
            status_code = request.form['statusList']
            title = request.form['title']
            subtitle = request.form['subtitle']
            author = request.form['author']
            description = request.form['description']
            new_book = Book(title=title,
                            subtitle=subtitle,
                            authors=author,
                            description=description,
                            status_id=status_code,
                            user_id=current_user.id)
            db.session.add(new_book)
            db.session.commit()
        else:
            print("pas 0 svp")
    return redirect(url_for('books.search'))


@books_bp.route('/book/<id_book>', methods=['GET', 'POST'])
def book(id_book):
    book_details = Book.query.filter_by(id=id_book).first()
    return render_template('book.html', user=current_user, book=book_details, background_color="page_book")


@books_bp.route('/delete_book/<id_book>', methods=['GET', 'POST'])
def delete_book(id_book):
    if request.method == 'POST':
        db.session.delete(Book.query.filter_by(id=id_book).first())
        db.session.commit()
        return redirect(url_for('books.home'))


@books_bp.route('/update_status', methods=["GET", "POST"])
def update_status():
    if request.method == "POST":
        id_book = request.form["id"]
        id_status = request.form["status"]
        db.session.query(Book).filter_by(id=id_book).update({'status_id': id_status})
        db.session.commit()
        return redirect(url_for('books.home'))
