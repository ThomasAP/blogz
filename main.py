from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://build-a-blog:password@localhost:3306/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(600))


    def __init__(self, name):
        self.name = name


@app.route("/", methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog = request.form['blog']
        blogs.append(blog)
        
    
    blogs = Blog.query.all()

    return render_template('newpost.html', title="Blogs In Space", blogs=blogs)

@app.route("/blog")
def blog():
    return render_template('blog')





if __name__ == ('__main__'):
    app.run()