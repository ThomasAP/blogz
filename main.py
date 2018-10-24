from flask import Flask, request, render_template, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    


    def __init__(self, title, body, author):
        self.title = title
        self.body = body
        self.author = author
        

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='author')

    def __init__(self, username, password):
        self.username = username
        self.password = password
    




@app.route("/", methods=['POST', 'GET'])
def index():
    return redirect("/blog")

@app.route("/blog")
def blog():
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)

@app.route("/blog-entry")
def blog_entry():
    id = int(request.args.get('id'))
    entry = Blog.query.get(id)

    return render_template('blog-entry.html', blog=entry )



@app.route("/signup", methods=['GET','POST'])



def signup():
    alpha="aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ"
    un_error = ''
    pwd_error = ''
    ver_error = '' 
    em_error = ''
    
    u_name=''
    p_word=''
    v_p_word=''
    e_mail=''
    
    user=''
    pwd=''
    ver=''
    email=''
    
    
    if request.method == 'POST':
        
        user = request.form['username']
        # Include validation for username
        #If User field is blank
        if user == '':
            un_error = "User must enter a username."
        
        #If length is greater than 20 or less than 3
        elif len(user) < 3 or len(user) > 20:
            un_error = "Username must be between 3 and 20 characters."
        
        #If username contains spaces or special characters
        for char in user:
            if char not in alpha:
                un_error = "Username can't use special characters or spaces."

        # Include validation for password       
        pwd = request.form['password']
        
        if pwd == '':
            pwd_error="User must enter a password."

        # Include validation for verify presence
        ver = request.form['verify']
        if ver == '':
            ver_error="User must verify password."
        
        # Include validation for password matching
        elif pwd != ver:
            ver_error="Passwords do not match."

        # Include validation for email formatting
        email = request.form['email']
        # Include validation for email
        confirm_at = 0
        confirm_dot = 0
        if email != '':
            for char in email:            
                if char == '@':
                    confirm_at += 1
                elif char == '.':
                    confirm_dot += 1
            if confirm_at != 1:
                em_error="Invalid Email: Missing '@'"
            
            if confirm_dot != 1:
                em_error="Invalid Email: Missing '.'"

        existing_user = User.query.filter_by(username=user).first()
        

        if (un_error + pwd_error + ver_error + em_error) != '':
            return render_template('index.html', 
            user_name_error=un_error, 
            password_error=pwd_error, 
            verify_error=ver_error, 
            email_error=em_error, u_name=user, p_word=pwd, v_p_word=ver, e_mail=email )    
        else:
            #If user creation doesn't return an error, check if user info matches any other user entry; if not, add new user to database.
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['user'] = username
                return redirect('/newpost.html')
            return render_template('greeting.html', uname=user)

    return render_template('newpost.html', u_name=user, p_word=pwd, v_p_word=ver, e_mail=email )



@app.route("/newpost", methods=['GET', 'POST'])
def newpost():
    title_error = ''
    body_error = ''

    if request.method == "POST":
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-body']

        if blog_title == '': #Return an error message if title is blank
            title_error = "Please fill in the title"
        if blog_body == '': #Return an error message if body is blank
            body_error = "Please fill in the body"

        #If either entry field returned an error, rerender form with errors populated
        if (title_error + body_error) != '':
            return render_template("newpost.html", title_error = title_error, body_error = body_error)
        else:
            new_post = Blog(blog_title, blog_body)
            db.session.add(new_post)
            db.session.commit()

        author = User.query.filter_by(username=session['user']).first() 
        #blogs = Blog.query.get()
        return render_template("blog-entry.html",title = "Blogs in Space", blog = new_post, blog_author =author )
    return render_template('newpost.html')




if __name__ == ('__main__'):
    app.run()
