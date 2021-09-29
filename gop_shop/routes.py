import os
from werkzeug.utils import secure_filename
from gop_shop import app
from flask import render_template, request
from gop_shop.models import Product, db
# from PIL import Image

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
        f = request.form
        file_name = request.files.get('image')
        filename = secure_filename(file_name.filename)
        file_name.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        p = Product(title=f.get('title'), price=f.get('price'), category=f.get('category'), availibility=f.get('availibility'),
        description=f.get('description'), image=file_name.filename)
        db.session.add(p)
        db.session.commit() 
    return render_template('add_product.html')