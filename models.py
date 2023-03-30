from flask_login import UserMixin
from sqlalchemy.orm import relationship
from __init__ import db


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
    confirmed = db.Column(db.Boolean, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    order = relationship("Order", back_populates="user")


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
    order_details = relationship("Order_Details", back_populates="product")
    review = relationship("Review", back_populates="product")


class Discount(db.Model):
    __tablename__ = "discounts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    percent_sale = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    order = relationship("Order", back_populates="discount")


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    discount_id = db.Column(db.Integer, db.ForeignKey("discounts.id"), nullable=True)
    order_date = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Float, nullable=False)
    user = relationship("User", back_populates="order")
    discount = relationship("Discount", back_populates="order")
    order_details = relationship("Order_Details", back_populates="order")


class Order_Details(db.Model):
    __tablename__ = "orders_details"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    product_size = db.Column(db.String(10), nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    order = relationship("Order", back_populates="order_details")
    product = relationship("Product", back_populates="order_details")


class Newsletter(db.Model):
    __tablename__ = "newsletter"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    confirmed = db.Column(db.Boolean, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)


class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=False)
    text = db.Column(db.String(1000), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    posted_on = db.Column(db.DateTime, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"))
    product = relationship("Product", back_populates="review")


# db.drop_all()
db.create_all()
