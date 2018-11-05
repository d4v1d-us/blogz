from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))

    def __init__(self, title, body):
        self.title = title
        self.body = body
        #self.id = id

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if title == '':

            flash("You should enter a Title for you Post")
            return render_template('newpost.html', title="Build a Blog", post_title=title, body=body)

        if body == '':

            flash("You should enter the Body for you Post")
            return render_template('newpost.html', title="Build a Blog", post_title=title, body=body)

        new_post = Blog(title, body)

        db.session.add(new_post)
        db.session.commit()

        postID = new_post.id
        post = Blog.query.filter_by(id=postID).first()
        return render_template('postdetail.html', title="Build a Blog", post=post)

        # posts = Blog.query.filter_by().all()
        # return render_template('blog.html', title="Build a Blog", posts=posts)

    if request.method == 'GET':

        #posts = Blog.query.filter_by().all()
        return render_template('newpost.html', title="Build a Blog")


@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method == 'POST' or request.method == 'GET':
        postID = request.args.get('id', default=None)
        if postID != None:
            post = Blog.query.filter_by(id=postID).first()
            return render_template('postdetail.html', title="Build a Blog", post=post)
        else:
            posts = Blog.query.filter_by().all()
            return render_template('blog.html', title="Build a Blog", posts=posts)


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        new_post = Blog(title, body)

        db.session.add(new_post)
        db.session.commit()

        posts = Blog.query.filter_by().all()

        return render_template('index.html', title="Build a Blog", posts=posts)

    if request.method == 'GET':

        posts = Blog.query.filter_by().all()
        return render_template('index.html', title="Build a Blog", posts=posts)


if __name__ == '__main__':
    app.run()
