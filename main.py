from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner
        #self.id = id

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10))
    password = db.Column(db.String(10))
    email = db.Column(db.String(120), unique=True)
    blogz = db.relationship('Blog', backref='owner')

    def __init__(self, email, password):
        self.email = email
        self.password = password
        #self.pw_hash = make_pw_hash(password)
        #self.id = id

@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'static']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/login' )

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user: #and check_pw_hash(password, user.pw_hash):
            session['email'] = email
            flash("Logged in", 'info')
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'danger')
    return render_template('login.html', title="Build a Blog")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            session['email'] = email
            return redirect('/')
        else:
            flash("The email <strong>{0}</strong> is already registered".format(email), 'danger')

    return render_template('register.html')

@app.route('/logout', methods=['POST'])
def logout():
    del session['email']
    return redirect('/')
    
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

        new_post = Blog(title, body, owner)

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

        new_post = Blog(title, body, owner)

        db.session.add(new_post)
        db.session.commit()

        posts = Blog.query.filter_by().all()

        return render_template('index.html', title="Build a Blog", posts=posts)

    if request.method == 'GET':

        posts = Blog.query.filter_by().all()
        return render_template('index.html', title="Build a Blog", posts=posts)


if __name__ == '__main__':
    app.run()
