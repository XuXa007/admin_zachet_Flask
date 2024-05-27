from flask import Flask, jsonify

app = Flask(__name__)


class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class Book:
    def __init__(self, id, title, author_id):
        self.id = id
        self.title = title
        self.author_id = author_id


authors = [Author(1, "George Orwell"), Author(2, "Aldous Huxley")]
books = [Book(1, "1984", 1), Book(2, "Brave New World", 2)]


@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({'books': [book.__dict__ for book in books], 'count': len(books)})


@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = next((book for book in books if book.id == id), None)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book.__dict__)


@app.route('/authors', methods=['GET'])
def get_authors():
    return jsonify([author.__dict__ for author in authors])


@app.route('/authors/<int:id>', methods=['GET'])
def get_author(id):
    author = next((author for author in authors if author.id == id), None)
    if author is None:
        return jsonify({'error': 'Author not found'}), 404
    return jsonify(author.__dict__)


@app.route('/check', methods=['GET'])
def check_service():
    return jsonify({'message': 'Service is running...'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
