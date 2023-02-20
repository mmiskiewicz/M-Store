from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, URL
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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


# db.drop_all()
# db.create_all()


@app.route('/')
def show_main_page():
    products = Product.query.all()
    return render_template("index.html", products=products)


if __name__ == "__main__":
    app.run(debug=True)
