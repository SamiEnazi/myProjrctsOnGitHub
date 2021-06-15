from flask import Flask, render_template, request, redirect, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

#look at method on line 27(get method): this is where the jsonfy output is.
mybooks = []

class books(db.Model):
    __tablename__ ='books'
    id = db.Column(db.Integer, primary_key=True,nullable=False)
    title = db.Column(db.String(128), unique=True, nullable=False)
    author = db.Column(db.String(128),nullable=False)
    type = db.Column(db.String(64), nullable=False)
    read = db.Column(db.Boolean,nullable = False,default = False)
    def __init__(self,title,author,type,read):
        self.title = title
        self.author = author
        self.type = type
        self.read = read


#deleted this because it does nothing 
# @app.route('/')
# def index():
#     return render_template('mybooks.html')


    
@app.route('/add-book')
def addBook():
    return render_template('add-book.html')


# TODO: implment a GET request to fetch all books

@app.route('/',methods=['GET'])
def index():
    allbooks = db.session.query(books).all()
    mybooks = []
    # use itration to get all books and jsonify it then return it on the site
    for book in allbooks:
        currentbook = {}
        currentbook['id'] = book.id
        currentbook['title'] = book.title
        currentbook['author'] = book.author
        currentbook['type'] = book.type
        currentbook['read'] = book.read
        mybooks.append(currentbook)
    print(mybooks)
    return render_template('mybooks.html',mybooks=mybooks)

# TODO: implment a POST request of adding a book 

@app.route('/add-book', methods=['POST'])
def submit():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        type = request.form['type']
        if title == '' or author == '':
            return render_template('main.html', message='Please enter required fields')
        
        data = books(title,author,type,False)
        db.session.add(data)
        db.session.commit()
        db.session.close()
        return redirect('/')
    
# TODO: implment a PUT request to mark the book as read

@app.route('/<int:id>', methods=['PUT'])
def readButton(id):
    book_to_update = db.session.query(books).filter(books.id==id).one_or_none()
    book_to_update.read = True
    db.session.commit()
    db.session.close()
    return render_template('mybooks.html')


# TODO: implment a Delete request to delete a book
@app.route('/<int:id>', methods=['DELETE'])
def deleteButton(id):
    book_to_delete = db.session.query(books).filter(books.id == id).one_or_none()
    db.session.delete(book_to_delete)
    db.session.commit()
    db.session.close()
    return render_template('mybooks.html')


# Default port:
if __name__ == '__main__':
    app.run(debug=True)