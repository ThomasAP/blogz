from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://build-a-blog-TP:password@localhost:8889/build-a-blog-TP'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1000))


    def __init__(self, title, body):
        self.title = title
        self.body = body


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




@app.route("/newpost", methods=['GET', 'POST'])
def newpost():
    title_error = ''
    body_error = ''

    if request.method == "POST":
        blog_title = request.form['blog-title']
        blog_body = request.form['blog-body']

        if blog_title == '': #Return and error message if title is blank
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

        #blogs = Blog.query.get()
        return render_template("blog-entry.html",title = "Blogs in Space", blog = new_post)
    return render_template('newpost.html')




if __name__ == ('__main__'):
    app.run()
