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
    username = db.Column(db.String(120), unique=True)
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
        username = request.form['username']
        password = request.form['password']

        if username == "" or password == "":
            flash('Please enter your Login', 'danger')
            return render_template('login.html', title="Blogz")
        else:
            user = User.query.filter_by(username=username).first()
            if not user:
                flash('Username does not exist', 'danger')
                return render_template('login.html', title="Blogz")

        user = User.query.filter_by(username=username, password=password).first()

        if user: #and check_pw_hash(password, user.pw_hash):
            session['email'] = user.email
            session['username'] = username
            flash("Logged in", 'info')
            return redirect('/newpost')
        else:
            flash('User Password incorrect', 'danger')
            return render_template('login.html', title="Blogz", username=username)
    return render_template('login.html', title="Blogz")

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        if username == None:
            username = ''

        #check username
        if username == '':
            flash("Hey Enter a Username!", 'danger')
            return render_template('register.html')

        if len(username) > 10 or len(username) < 3:
            flash("Hey Username should be 3 to 10 in length!", 'danger')
            return render_template('register.html')


        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            flash("We already have the username <strong>{0}!!</strong>".format(username), 'danger')

    return render_template('register.html')

@app.route('/logout', methods=['POST'])
def logout():
    del session['email']
    del session['username']
    return redirect('/')

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if title == '':

            flash("You should enter a Title for you Post")
            return render_template('newpost.html', title="Blogz", post_title=title, body=body)

        if body == '':

            flash("You should enter the Body for you Post")
            return render_template('newpost.html', title="Blogz", post_title=title, body=body)

        new_post = Blog(title, body, owner)

        db.session.add(new_post)
        db.session.commit()

        postID = new_post.id
        post = Blog.query.filter_by(id=postID).first()
        return render_template('postdetail.html', title="Blogz", post=post)

        # posts = Blog.query.filter_by().all()
        # return render_template('blog.html', title="Build a Blog", posts=posts)

    if request.method == 'GET':

        #posts = Blog.query.filter_by().all()
        return render_template('newpost.html', title="Blogz")


@app.route('/blog', methods=['POST', 'GET'])
def blog():

    if request.method == 'POST' or request.method == 'GET':
        postID = request.args.get('id', default=None)
        if postID != None:
            post = Blog.query.filter_by(id=postID).first()
            return render_template('postdetail.html', title="Blogz", post=post)
        else:
            posts = Blog.query.filter_by().all()
            return render_template('blog.html', title="Blogz", posts=posts)


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        new_post = Blog(title, body, owner)

        db.session.add(new_post)
        db.session.commit()

        posts = Blog.query.filter_by().all()

        return render_template('index.html', title="Blogz", posts=posts)

    if request.method == 'GET':

        posts = Blog.query.filter_by().all()
        return render_template('index.html', title="Blogz", posts=posts)


if __name__ == '__main__':
    app.run()
