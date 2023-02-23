from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from sqlalchemy.orm import relationship
from forms import LoginForm, RegisterForm
from bs4 import BeautifulSoup
from flask_wtf import FlaskForm
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, URL
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    address = db.Column(db.String(100))
    postal_code = db.Column(db.String(10))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    cart = relationship("Cart", back_populates="user")


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.String(6), nullable=False)
    category = db.Column(db.String(25), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    original_price = db.Column(db.Float, nullable=False)
    current_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    additional_description = db.Column(db.String(1000), nullable=False)
    available_sizes = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    img_url2 = db.Column(db.String(250), nullable=True)
    img_url3 = db.Column(db.String(250), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    cart = relationship("Cart", back_populates="product")


class Cart(db.Model):
    __tablename__ = "shopping_cart"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    size = db.Column(db.String(6), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    product = relationship("Product", back_populates="cart")
    user = relationship("User", back_populates="cart")

# db.drop_all()
db.create_all()



@app.route('/')
def show_main_page():
    products = Product.query.all()
    return render_template("index.html", products=products)


@app.route('/product/<int:product_id>', methods=["GET", "POST"])
def view_product(product_id):

    requested_product = Product.query.get(product_id)
    if request.method == 'POST':
        print("weszlo")
        cart = Cart(
            product_id=requested_product.id,
            size=request.form["size"],
            quantity=request.form["quantity"]
        )
        db.session.add(cart)
        db.session.commit()
        return render_template("product.html", product=requested_product)
    # else:
    #     if "plus" not in request.form and "minus" not in request.form:
    #         return render_template("product.html", product=requested_product)
    else:
        return render_template("product.html", product=requested_product)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        # Email doesn't exist or password incorrect.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('show_main_page'))
    return render_template("login.html", form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            print(User.query.filter_by(email=form.email.data).first())
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
        name=form.name.data,
        surname=form.surname.data,
        email=form.email.data,
        password=hash_and_salted_password,
        address=form.address.data,
        postal_code=form.postal_code.data,
        city=form.city.data,
        country=form.country.data
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("show_main_page"))


    return render_template("register.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('show_main_page'))


if __name__ == "__main__":
    app.run(debug=True)
