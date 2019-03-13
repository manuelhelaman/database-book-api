from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_heroku import Heroku

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dsnyvbvkikwyto:a39a70ed30240e469f39136620d26f98c280199e7ca97da9c98f5a1c38f03ef1@ec2-54-163-234-88.compute-1.amazonaws.com:5432/d9v3sqhdkru34u'

heroku = Heroku(app)
db = SQLAlchemy(app)

class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    author = db.Column(db.String(80))

    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __repr__(self):
        return '<Title %r>' % self.title        

@app.route('/')
def home():
    return "<h1>Hi from Flask<h1>"

@app.route('/book/input', methods=['POST'])
def books_input():
    if request.content_type == 'application/json':
        post_data = request.get_json()
        title = post_data.get('title')
        author = post_data.get('author')
        reg = Books(title, author)
        db.session.add(reg)
        db.session.commit()
        return jsonify("Data Posted")
    return jsonify('Something went wrong')

@app.route('/books', methods=['GET'])
def return_books():
    all_books = db.session.query(Books.id, Books.title, Books.author).all()
    return jsonify(all_books)

@app.route('/update_book/<id>', methods=["PUT"])
def book_update(id):
    if request.content_type == 'application/json':
        put_data = request.get_json()
        title = put_data.get('title')
        author = put_data.get('author')    
        record = db.session.query(Books).get(id)
        record.title = title
        record.author = author
        db.session.commit()
        return jsonify("Completed Update")
    return jsonify("Update Failed")    

@app.route('/book/<id>', methods=["GET"])
def return_single_book(id):
    one_book = db.session.query(Books.id, Books.title, Books.author).filter(Books.id == id).first()
    return jsonify(one_book)    

@app.route('/delete/<id>', methods=["DELETE"])
def book_delete(id):
    if request.content_type == 'application/json':
        record = db.session.query(Books).get(id)
        db.session.delete(record)
        db.session.commit()
        return jsonify("Completed Delete action")
    return jsonify("Delete Failed")    

if __name__ == '__main__':
    app.debug = True
    app.run()