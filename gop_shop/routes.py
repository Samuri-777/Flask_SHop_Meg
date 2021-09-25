from gop_shop import app
from flask import render_template

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/base")
def base():
     return render_template('base.html')


@app.route("/blog")
def blog():
    return render_template("blog.html")
