from flask_migrate import current
from werkzeug.utils import secure_filename
from gop_shop import app
from flask import render_template, request, redirect, url_for,flash
from gop_shop.models import Product, db, User
from PIL import Image
from flask_login import login_user, logout_user, current_user
from gop_shop.forms import RegistrationForm

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
        image = request.files.get('image')
        if image:
            file_name = image.filename
            image = Image.open(image)
            image.save('gop_shop/static/img/product' + file_name)
        p = Product(title=f.get('title'), price=f.get('price'), description=f.get('description'), availibility=f.get('availibility'),
        category=f.get('category'), image=file_name)
        db.session.add(p)
        db.session.commit() 
    return render_template('add_product.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
       return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)


@app.route('/login', methods=(['GET', 'POST']))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user and user.password == request.form.get('password'):
            login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/products/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get(product_id)
    print(product)
    return render_template('product_detail.html', product=product)