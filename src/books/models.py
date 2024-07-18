from src import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # isbn = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    authors = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, subtitle, authors, description, status_id, user_id):
        # self.isbn = isbn
        self.title = title
        self.subtitle = subtitle
        self.authors = authors
        self.description = description
        self.status_id = status_id
        self.user_id = user_id


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), nullable=False)
    books = db.relationship('Book')


