from flask_login.utils import login_required
from gop_shop import app
from flask import render_template, request, redirect, url_for,flash
from gop_shop.models import Product, db, User, Post, Comment, Buy
from PIL import Image
from flask_login import login_user, logout_user, current_user
from gop_shop.forms import RegistrationForm, PostForm

@app.route("/")
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route("/base")
def base():
     return render_template('base.html')


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


@app.route("/blog")
def blog():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.data_posted.desc()).paginate(page=page,  per_page=1)
    return render_template('blog.html', posts=posts)


@app.route('/new_post', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        image = request.files.get('image')
        if image:
            file_name =image.filename
            image.save('gop_shop/static/img/blog/' + file_name)
            post = Post(title=form.title.data,
                        content=form.content.data, author=current_user, image=file_name)
            db.session.add(post)
            db.session.commit()
            flash('Пост был создан!', 'saccess')
            return redirect(url_for('blog'))
    return render_template('new_post.html', form=form)



@app.route('/blog/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    post = Post.query.get(post_id)
    comments = Comment.query.order_by(Comment.data_posted.desc()).all()
    if request.method == 'POST':
        comment = Comment(name=request.form.get('name'), subject=request.form.get(
            'subject'),email=request.form.get('email'), message=request.form.get('message'), post=post)
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий был добавлен!', 'saccess')
    return render_template('post_detail.html', post=post, comments=comments)
    

@app.route('/products/<int:product_id>/buy', methods=['GET', 'POST'])
def buy(product_id):
    product = Product.query.get(product_id)
    if request.method == "POST":
        f = request.form
        b = Buy(name=f.get('name'), adress=f.get('adress'), email=f.get('email'), product=product)
        db.session.add(b)
        db.session.commit() 
    return render_template('buy.html')


@app.route('/buys')
def buys():
    buys = Buy.query.all()
    return render_template('buys.html', buys=buys)