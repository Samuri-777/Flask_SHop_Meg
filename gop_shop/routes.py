from gop_shop import app
from flask import render_template, request
from gop_shop.models import Product, db
from PIL import Image

@app.route("/")
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route("/base")
def base():
     return render_template('base.html')


@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == "POST":
        file_name = request.files.get('image')

        f = request.form
        p = Product(title=f.get('title'), price=f.get('price'), category=f.get('category'), availibility=f.get('availibility'),
        description=f.get('description'), image=file_name)
        db.session.add(p)
        db.session.commit() 
    return render_template('add_product.html')