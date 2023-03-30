from flask_login import UserMixin
from sqlalchemy.orm import relationship
from __init__ import db
import datetime


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

# Adding some sample data for PostgreSQL database

new_discount = Discount(
    name="SALE20",
    percent_sale=20,
    expiration_date=datetime.date(2030, 3, 15)
)
db.session.add(new_discount)
db.session.commit()

new_product = Product(
    name="Regular Fit Linen-blend shirt",
    sex="Men",
    category="Shirts",
    original_price=155.00,
    current_price=100.00,
    description="Regular-fit shirt in a cotton and linen weave with a turn-down collar, classic front and yoke at the back. Long sleeves with buttoned cuffs and a sleeve placket with a link button. Cotton and linen blends combine the softness of cotton with the sturdiness of linen, creating a beautiful, textured fabric that is breathable and drapes perfectly.",
    additional_description="Linen 52%, Cotton 48%",
    available_sizes="'XS':4, 'S':4, 'M':9, 'L':10, 'XL':29, 'XXL':1",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F65%2F18%2F6518ab24b8ee8bf81b835b3e632004cc49907aae.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Ffe%2F5a%2Ffe5aaead376ddf823652ee4f8129cf59c17900a7.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fd4%2F56%2Fd45685dde1234aef192e40109b0ec9a65516e392.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Slim Fit Easy-iron shirt",
    sex="Men",
    category="Shirts",
    original_price=199.99,
    current_price=149.99,
    description="Slim-fit shirt in woven fabric with an easy-iron finish. Turn-down collar, classic front and darts and a yoke at the back. Long sleeves with adjustable buttoning at the cuffs and a sleeve placket with a link button. Gently rounded hem.",
    additional_description="Polyester 65%, Cotton 35%",
    available_sizes="'M':9, 'L':10, 'XL':29, 'XXL':1",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F44%2Fc2%2F44c2b04b3b6019b91a58db1b5ee07b0d54503432.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F40%2Fd9%2F40d996887e7fcfd1efe8c9e88f45d60d62da9a5a.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fcb%2F54%2Fcb5402b35a419d85c46c37a726388c386a39f5b7.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Regular Fit Oxford shirt",
    sex="Men",
    category="Shirts",
    original_price=149.99,
    current_price=99.99,
    description="Regular-fit shirt in Oxford cotton with a button-down collar, classic front, yoke at the back and an open chest pocket. Long sleeves with buttoned cuffs and a sleeve placket with a link button. Gently rounded hem.",
    additional_description="Cotton 100%",
    available_sizes="'S':9, 'L':10, 'XXL':1",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F64%2F4e%2F644e331d8d91a5795d44a64acc0757dd92cd61f2.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F3e%2F67%2F3e671c06e9420a4f9a9ad03f46ec257a2839db5d.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F6c%2F29%2F6c290410bd6016f51ad67f1c901bae67d0e6ecf2.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Linen shirt",
    sex="Women",
    category="Shirts",
    original_price=99.99,
    current_price=49.99,
    description="Shirt in airy linen with a collar, buttons down the front and a yoke at the back. Gently dropped shoulders, long sleeves with buttoned cuffs, a patch chest pocket and a rounded hem. Longer at the back.",
    additional_description="Linen 100%",
    available_sizes="'XS':4, 'S':9, 'M':2, 'L':10, 'XL':4, 'XXL':1",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Ff0%2F5b%2Ff05b0a482c2d6b87776d101d790c501483b18080.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F91%2F8f%2F918fda1200880c0227f7f48907290f9c06bacaee.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fd0%2Fb3%2Fd0b319b40b215563954658a8375a0b5fa0e56aad.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Patterned shirt",
    sex="Women",
    category="Shirts",
    original_price=249.99,
    current_price=129.99,
    description="Shirt in a patterned weave with a collar, buttons down the front and a yoke at the back. Relaxed fit with dropped shoulders, long sleeves with buttoned cuffs, and a rounded hem. Slightly longer at the back.",
    additional_description="Polyester 100%",
    available_sizes="'M':4, 'L':10, 'XXL':1",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F85%2F2b%2F852b5ed665a1eccd21b0cd257ba308a20ab31427.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F30%2Fda%2F30daf8261555971b3c1647281ca1c3896bde9743.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F4b%2F82%2F4b82caccd9dd7944de2c8a2971da922cb02230db.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Oxford shirt",
    sex="Women",
    category="Shirts",
    original_price=129.99,
    current_price=89.99,
    description="Shirt in washed Oxford cotton with a collar, buttons down the front and a yoke with a hanger at the back. Relaxed fit with dropped shoulders, long sleeves with buttoned cuffs, and a rounded hem. Slightly longer at the back.",
    additional_description="Cotton 100%",
    available_sizes="'XS':4, 'S':9, 'M':4, 'L':10, 'XXL':1",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F28%2F26%2F2826447aaf893ad7f50802d6bee366b572ad2252.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fc7%2F3e%2Fc73e1a5596c2e946930e77abb37a3ae65cce7835.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F42%2F4c%2F424c01b2cdfbb92cc2f42a46dbb66e4e8a3db021.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Relaxed Resort Short Sleeve Shirt",
    sex="Men",
    category="Shirts",
    original_price=149.99,
    current_price=79.99,
    description="A relaxed-fit buttoned short sleeve shirt with a resort collar made from a lightweight lyocell and cotton twill. It has a front patch pocket, and a straight hemline.",
    additional_description="Lyocell 78%, Cotton 22%",
    available_sizes="'S':9, 'L':10, 'XXL':1",
    img_url="https://lp.weekday.com/app003prod?set=quality%5B79%5D%2Csource%5B%2F32%2F28%2F3228adbf4da447fab1fe24aa6142a17d1df2c60f.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp.weekday.com/app003prod?set=quality%5B79%5D%2Csource%5B%2Fa7%2F9f%2Fa79f41ccd840e7caee44acf121d739f0ad67eabf.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp.weekday.com/app003prod?set=quality%5B79%5D%2Csource%5B%2Fd1%2F3d%2Fd13dd553e733faa1fab31b2b4d9c2f3b6b553efe.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Relaxed Fit Twill shirt",
    sex="Men",
    category="Shirts",
    original_price=119.99,
    current_price=39.99,
    description="Shirt in soft, checked cotton twill with a turn-down collar, classic front and yoke at the back. Relaxed fit with long sleeves with buttoned cuffs and a sleeve placket with a link button, open chest pockets and a rounded hem.",
    additional_description="Cotton 100%",
    available_sizes="'S':9, 'M':2, 'L':10, 'XL':3, 'XXL':1",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Ffc%2F50%2Ffc50762ea096ebaa13a95ca151ed8c4366ecce24.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F9e%2F00%2F9e000251233f60770f9beb1529e8a5bebe478f18.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F22%2Fd2%2F22d2cb93d939f7eacf4ac6a745275b291e57a30f.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Slim Jeans",
    sex="Men",
    category="Jeans",
    original_price=149.99,
    current_price=69.99,
    description="5-pocket jeans in cotton denim with a slight stretch for good comfort. Straight leg and a slim fit from the waist through the thigh to the hem. Regular waist and a zip fly. Easily styled for sleek or sporty.",
    additional_description="Cotton 99%, Elastane 1%",
    available_sizes="'XS': 6, 'S':9, 'M':2, 'L':10, 'XL':3, 'XXL':1",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fe1%2Fb9%2Fe1b93ebc0ec5acf041c9df6515d545a42cf012c3.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F13%2F5b%2F135b1334cbe5d9c65d8d23dfa8740fd293029c67.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F63%2F84%2F6384eeaa6598fcd9aa096c3a368336749236384e.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Freefit® Slim Jeans",
    sex="Men",
    category="Jeans",
    original_price=249.99,
    current_price=149.99,
    description="5-pocket jeans in denim with a slight stretch for good comfort. Straight leg and a slim fit from the waist through the thigh to the hem. Regular waist and a zip fly. Made using Lycra® Freefit® technology for soft, super-generous stretch, maximum mobility and optimal comfort.",
    additional_description="Cotton 90%, Elastomultiester 8%, Elastane 2%",
    available_sizes="'XS': 6, 'XL':3, 'XXL':1",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fe0%2F78%2Fe078afdc666030c25ee9062e862b95a8c6a8d5c1.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fd5%2F52%2Fd5520cdd7b7a2f2438729a5d56f7d8571b5a44e6.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fb1%2Fa6%2Fb1a6797846739bb4f94672a3d11031a15bba0ea3.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Slim Jeans",
    sex="Men",
    category="Jeans",
    original_price=249.99,
    current_price=129.99,
    description="5-pocket jeans in cotton denim with a slight stretch for good comfort. Straight leg and a slim fit from the waist through the thigh to the hem. Regular waist and a zip fly. Easily styled for sleek or sporty.",
    additional_description="Cotton 99%, Elastane 1%",
    available_sizes="'M': 6, 'L':3, 'XXL':1",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fcc%2F7c%2Fcc7c1b59ebbab956adaf4872c9656b2473022d81.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Faf%2F6b%2Faf6bc87d1509ecc66cad10993850f727fb448dd0.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fd3%2F04%2Fd304c39f9883f20595081a6f76256ba96ad43cc8.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Slim High Ankle Jeans",
    sex="Women",
    category="Jeans",
    original_price=129.99,
    current_price=89.99,
    description="5-pocket, slim-fit jeans in slightly stretchy denim with a high waist, zip fly and button and straight, ankle-length legs. This garment is made from innovative fabric containing CIRCULOSE® viscose and recycled cotton. It is finished using lower-impact washing techniques.",
    additional_description="Cotton 69%, Viscose 30%, Elastane 1%",
    available_sizes="'XS':3, 'S':6, 'M': 6, 'L':3, 'XL':3, 'XXL':1",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fa9%2F06%2Fa906fda8ca6d91d46af75022323755cfe0744882.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F0f%2F0e%2F0f0eba7bae48769ca38b3d37c6a6796ccf45346d.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fe8%2Fc2%2Fe8c241159e87fd4c26da35ac61ac62052a41291a.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Vintage Straight High Jeans",
    sex="Women",
    category="Jeans",
    original_price=189.99,
    current_price=139.99,
    description="5-pocket, ankle-length jeans in sturdy denim with a high waist, zip fly and button and straight legs.",
    additional_description="Cotton 99%, Elastane 1%",
    available_sizes="'S':6, 'M': 6, 'L':3",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F0d%2Ff8%2F0df8cb03c7ad72a9ae731ce33e4435a54e5ffbc1.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5Bladies_jeans_straight%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fa2%2F8d%2Fa28db3cfcd15fed88d86d46a9d1d852e5f018ec6.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5Bladies_jeans_straight%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B2%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fdd%2Ffe%2Fddfe935a3eead8dff7bcd50af2f0c3c47444ffb3.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5Bladies_jeans_straight%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="90s Baggy High Cargo Jeans",
    sex="Women",
    category="Jeans",
    original_price=139.99,
    current_price=119.99,
    description="Relaxed-fit jeans in sturdy cotton denim with a high waist, low crotch, zip fly and button and straight, extra-long legs. Front and back pockets and flap leg pockets.",
    additional_description="Cotton 100%",
    available_sizes="'XS':3, 'S':6, 'M': 6, 'L':3",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F02%2F06%2F0206448af3e306e1ddb576bfac9402ebb165e951.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F48%2Ffb%2F48fb71b0d2b7c6ce1f50dccd6a3e18ac2476aadb.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fbc%2F95%2Fbc953326be854107af42aefd017c467487afbb78.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Linen jacket Slim Fit",
    sex="Men",
    category="Blazers",
    original_price=499.99,
    current_price=299.99,
    description="Single-breasted jacket in a linen weave with narrow notch lapels, a decorative buttonhole, a chest pocket, flap front pockets and two inner pockets. Slim fit with two buttons at the front, decorative buttons at the cuffs and a single back vent. Lined. Fabric made from linen is breathable, beautiful both ironed and wrinkled, and softens over time.",
    additional_description="Linen 100%",
    available_sizes="'XS':3, 'S':6, 'M': 6, 'L':3, 'XL':7, 'XXL':6",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F03%2Fa9%2F03a904468cd512fa379da5133db87e566469a379.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Faf%2Ffb%2Faffb57666a51eb8199a9a1a5daff4d2886060351.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F78%2F48%2F78480525b9b9bd6df035c0d8675e4c12fe3ae31d.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Relaxed Fit Lyocell jacket",
    sex="Men",
    category="Blazers",
    original_price=399.99,
    current_price=249.99,
    description="Relaxed-fit jacket in a lyocell weave with notch lapels and a two-button fastening at the front. Jetted front pockets with a flap, a chest pocket, two inner pockets, decorative buttons at the cuffs and a single back vent. Lined. Fabric made from lyocell is super soft, wrinkle resistant and drapes beautifully.",
    additional_description="Polyester 100%",
    available_sizes="'XS':3, 'M': 6, 'L':3",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F0e%2Fc3%2F0ec3b363b2d34c29414393b9d0c2e0e47eadd928.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F83%2Fe3%2F83e30071e00efefd7186ef69a323c17ae956e68c.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F83%2Fae%2F83aef00c681d2fe33500dd754c2c3f0911d32206.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Jacket Slim Fit",
    sex="Men",
    category="Blazers",
    original_price=349.99,
    current_price=279.99,
    description="Single-breasted jacket in a stretch weave with narrow notch lapels with a decorative buttonhole, a chest pocket, flap front pockets and one inner pocket. Two buttons at the front, decorative buttons at the cuffs and a single back vent. Lined. Slim fit that tapers at the chest and waist which, combined with slightly narrower sleeves, creates a fitted silhouette.",
    additional_description="Polyester 69%, Viscose 29%, Elastane 2%",
    available_sizes="'XS':3, 'S': 6, 'M':3",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Faf%2Faa%2Fafaa41f445cea743aae7935ed954120d3fa6d38b.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F7e%2Fe5%2F7ee562bab094a5d725dfd692eb7dec1ae3bf4283.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fa1%2F89%2Fa18939340ba21c191098a7fd14d85c1a9259539b.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Double-breasted blazer",
    sex="Women",
    category="Blazers",
    original_price=349.99,
    current_price=269.99,
    description="Double-breasted blazer in woven fabric with notch lapels and buttons at the front. Shoulder pads, long sleeves and jetted front pockets. Lined.",
    additional_description="Polyester 76%, Viscose 18%, Elastane 6%",
    available_sizes="'XS':3, 'S': 6, 'M':3, 'L':6, 'XL':5, 'XXL':5",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Feb%2F05%2Feb05ab237d8bb05bf243d81804ec2a553b8147ab.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F59%2Fcf%2F59cf44415f39ab6a83816dd86544b334526adecc.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F4d%2F8c%2F4d8c7407262b608167446115745693f3227b946d.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Double-breasted blazer",
    sex="Women",
    category="Blazers",
    original_price=349.99,
    current_price=269.99,
    description="Double-breasted blazer in woven fabric with notch lapels and buttons at the front. Shoulder pads, long sleeves and jetted front pockets. Lined.",
    additional_description="Viscose 92%, Polyester 8%",
    available_sizes="'XS':3,'XXL':5",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fff%2Fa5%2Fffa59423527c5552efdb22018e12889a0371c4bd.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fe3%2F4a%2Fe34aabcec30f43875e6c51c0c7a7e863a36ebdff.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F54%2F6a%2F546a144fddae3eec73debcc088d56f0adb413618.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Single-breasted jacket",
    sex="Women",
    category="Blazers",
    original_price=249.99,
    current_price=129.99,
    description="Single-breasted jacket in woven fabric with notch lapels and a single button at the front. Flap welt front pockets, decorative buttons at the cuffs and a single back vent. Lined in satin made from recycled polyester.",
    additional_description="Polyester 62%, Viscose 34%, Elastane 4%",
    available_sizes="'S':6, 'M':3, 'L':6, 'XXL':5",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F3a%2F80%2F3a8048b7e669cf226c6bbc53dd61af5bde7bd561.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F44%2F6d%2F446d61cda37707a58a503d631c70d7eca6bb45bb.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fd9%2F5b%2Fd95bab6154049636f036034add285249d5c1d129.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Regular Fit Round-neck T-shirt",
    sex="Men",
    category="T-shirts",
    original_price=39.99,
    current_price=29.99,
    description="Regular-fit T-shirt in soft cotton jersey with a round, rib-trimmed neckline and a straight hem.",
    additional_description="Cotton 100%",
    available_sizes="'XS':4, 'S':6, 'M':3, 'L':6, 'XL':5, 'XXL':5",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F61%2F03%2F61031c2fd05624e684820883d878e514e69d0079.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5Bmen_tshirtstanks_shortsleeve%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F68%2F23%2F6823ade9256e2f87cd30134af678883e5953fb2c.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5Bmen_tshirtstanks_shortsleeve%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F5f%2F90%2F5f90364e7ef2bd00e68ea58804d84932687f1f4a.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5Bmen_tshirtstanks_shortsleeve%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Slim Fit Pima cotton T-shirt",
    sex="Men",
    category="T-shirts",
    original_price=59.99,
    current_price=49.99,
    description="Slim-fit T-shirt in soft pima cotton jersey. Round neckline with a finely-ribbed trim and a straight-cut hem.",
    additional_description="Cotton 100%",
    available_sizes="'L':6, 'XL':5, 'XXL':5",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F29%2F51%2F29515a3f571e04f27b8f56fee554c142cb3b3f51.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F60%2Fa8%2F60a828bede4489cc01cb1e77cf713b6a32e1da19.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F47%2F77%2F477717653ede3026fdb6ffe2ac24a728801fb7c7.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="T-shirt Long Fit",
    sex="Men",
    category="T-shirts",
    original_price=39.99,
    current_price=19.99,
    description="Long, round-necked T-shirt in soft jersey with a curved hem.",
    additional_description="Cotton 100%",
    available_sizes="'S':6, 'L':5, 'XL':5",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fc5%2Fe4%2Fc5e421386883c2e73ff0cc57208d74f9b999b023.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fd9%2Fcc%2Fd9cc9c95d244d78b31fecfa25dcb458561c21ec5.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F68%2F49%2F68490c7c24f937541f71308d8857fb2b487688e6.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Cotton T-shirt",
    sex="Women",
    category="T-shirts",
    original_price=29.99,
    current_price=19.99,
    description="Straight-cut T-shirt in soft cotton jersey with a round, rib-trimmed neckline and gently dropped shoulders.",
    additional_description="Cotton 100%",
    available_sizes="'XS':5, 'S':6, 'M':4, 'L':5, 'XL':5, 'XXL':3",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F2d%2F60%2F2d60757fa68eed4aabb7cfae6adbe576fcf951b0.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fce%2Fdb%2Fcedb5aecd8abedf6ea92e13cdefef1f8a10c4b57.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fa0%2Fd8%2Fa0d888a1faaae8b6f66224996089fce4d97d3b42.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Crew-Neck T-shirt",
    sex="Women",
    category="T-shirts",
    original_price=59.99,
    current_price=49.99,
    description="As part of the Jersey Yarn Project, this T-shirt is custom-knit from a smooth, compact and naturally whiter long staple cotton, collected from one single-fibre source. Designed with a regular fit of single jersey with a ribbed piping around the crew-neck.",
    additional_description="Cotton 100%",
    available_sizes="'S':6, 'M':4, 'XXL':3",
    img_url="https://lp.arket.com/app006prod?set=quality%5B79%5D%2Csource%5B%2F0f%2Ffe%2F0ffe077c4f982d42d4ed55853ecd73068d0478f3.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp.arket.com/app006prod?set=quality%5B79%5D%2Csource%5B%2Fcf%2F22%2Fcf22aa1fbafa1105ba3fd36c7be58769ae97f2ab.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp.arket.com/app006prod?set=quality%5B79%5D%2Csource%5B%2F5e%2F6c%2F5e6c997704bf76a1ac303f9a9507a2a54747cceb.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Slim Fitted T-shirt",
    sex="Women",
    category="T-shirts",
    original_price=69.99,
    current_price=39.99,
    description="A go-to everyday t-shirt with a slim fit made from a soft cotton jersey and a touch of recycled elastane for extra stretch and comfort. It has a round neck and straight hems.",
    additional_description="Cotton 90%, Elastane 10%",
    available_sizes="'M':6, 'L':4, 'XXL':3",
    img_url="https://lp.weekday.com/app003prod?set=quality%5B79%5D%2Csource%5B%2F88%2F44%2F8844c90b6957c72ea4085553af8fc6ba5f8e9dbb.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp.weekday.com/app003prod?set=quality%5B79%5D%2Csource%5B%2Fff%2Fd3%2Fffd3842da65040a50b27596a692a46d0564a3337.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp.weekday.com/app003prod?set=quality%5B79%5D%2Csource%5B%2F25%2Fc2%2F25c229e237c315680ca01bdd7a2428660d48db46.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Linen-blend dress",
    sex="Women",
    category="Dresses",
    original_price=169.99,
    current_price=99.99,
    description="Calf-length dress in a linen and cotton weave with a sweetheart neckline and narrow, adjustable shoulder straps. Wide smocking at the back, a gathered seam at the waist and a flared skirt. Lined.",
    additional_description="Linen 52%, Cotton 48%",
    available_sizes="'XS':5, 'S':3, 'M':6, 'L':4, 'XL':6, 'XXL':3",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F89%2F0d%2F890dcdc0808869683ea00bec1a19f32008adb680.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F42%2F78%2F427892c99f3e073cfb9eaa7378f9045b7751cdff.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F6c%2F13%2F6c13e8a4f935de00b0e1e972cfea7c004433658f.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Shirt dress",
    sex="Women",
    category="Dresses",
    original_price=129.99,
    current_price=89.99,
    description="Calf-length, loose-fit dress in a patterned viscose weave with a collar and concealed buttons at the front. Long raglan sleeves with a slit and button at the cuffs. Skirt with wide, gathered tiers for added width. Unlined.",
    additional_description="Viscose 100%",
    available_sizes="'XS':5, 'S':3, 'M':6, 'L':4",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F76%2F07%2F7607eef0214f6d1d4c4b9322ead9f7bb07792cf7.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fc9%2Fba%2Fc9ba3caa1f7c872b094936ad367632bf4739a1a1.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F9c%2Ff5%2F9cf5c6a2cea7c1db427b3945fb1365600e0e2694.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Buttoned tie-belt dress",
    sex="Women",
    category="Dresses",
    original_price=189.99,
    current_price=129.99,
    description="Ankle-length dress in a viscose blend weave with a deep V-neckline and covered buttons down the front. Long, raglan cut balloon sleeves with narrow, covered elastication at the cuffs. Tie belt at the waist and a gathered tier at the hem to add width and volume. Unlined.",
    additional_description="Viscose 82%, Polyamide 18%",
    available_sizes="'XS':5, 'XL':3",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F9a%2F45%2F9a450ecb25c9d7ae6a2d90cd984c2a426cac40c6.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F10%2F3f%2F103f7c0113faa904c15fc4c819559b1ead4611cb.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fb5%2F1d%2Fb51ddf7af2ec6938aabb2e6a0b77674bf0b8a9c3.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Embroidered dress",
    sex="Women",
    category="Dresses",
    original_price=139.99,
    current_price=119.99,
    description="Ankle-length dress in woven fabric with tone-on-tone embroidery and broderie anglaise. Loose fit with a deep, V-shaped neckline and long, voluminous balloon sleeves in a raglan cut with narrow elastication at the cuffs. Gathered seam under the bust and at the back of the waist. Softly draping, voluminous skirt. Unlined.",
    additional_description="Viscose 90%, Polyester 10%",
    available_sizes="'M':5, 'L':3, 'XL':5, 'XXL':7",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fe7%2F42%2Fe742ac14a9df0652a58bc9d846d272fda6fe0876.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F85%2Fe8%2F85e8f3753dec7afdd59c82707a8045dce2cb7970.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F1d%2Fc9%2F1dc9933c10ad0d4e56d2b2cbeac975c14255c3e9.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Flounce-trimmed kaftan dress",
    sex="Women",
    category="Dresses",
    original_price=169.99,
    current_price=139.99,
    description="Calf-length kaftan dress in woven fabric with a V-shaped opening at the front and a yoke with pleats at the back. Loose fit with dropped shoulders and long, extra-wide, voluminous sleeves. Wide, detachable tie belt at the waist and wide flounces at the cuffs and down each side seam. Partly lined.",
    additional_description="Lyocell 77%, Polyamide 23%",
    available_sizes="'XS':5, 'S':3, 'M':5, 'XXL':7",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fed%2F38%2Fed38ff14b0f1ff250accdb3d82eecbece22a02a4.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Ff4%2F96%2Ff4960f8ecec63f715620e36edf6b213244ddbf9a.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F68%2Fa0%2F68a02ad9cbf2d9a918c5b9194f7106ef44e653c2.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Broderie anglaise beach dress",
    sex="Women",
    category="Dresses",
    original_price=179.99,
    current_price=129.99,
    description="Short beach dress in cotton poplin with broderie anglaise. Deep, V-shaped neckline at the front and back and narrow, horizontal ties at the back of the neck. Flutter sleeves, a gathered seam at the waist and a gently flared skirt. Unlined.",
    additional_description="Cotton 100%",
    available_sizes="'M':5, 'L':3, 'XL':5, 'XXL':7",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F4d%2Fa0%2F4da037e9b7a9a50095d083b5116e94495fc29f1c.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F57%2Fdc%2F57dcb697639242e15c414f43199d74aade369d9a.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F38%2F4d%2F384dc6f5b41c515e37e6e14beeea81d1f468505d.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Cotton cardigan",
    sex="Men",
    category="Cardigans",
    original_price=169.99,
    current_price=129.99,
    description="Long-sleeved cardigan in fine-knit cotton with a V-neck, buttons down the front and ribbing around the neckline, cuffs and hem.",
    additional_description="Cotton 100%",
    available_sizes="'XS':5, 'S':6, 'M':7, 'L':3, 'XL':5, 'XXL':7",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F54%2F4f%2F544fc5cd182c4030cdb4e58a8a0786fa8f033082.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Feb%2Fd5%2Febd58edf40627de9a4abf6827f148db35941b8fe.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fe5%2F58%2Fe558bea23acd80791aa9939b6780bae29d1c0277.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Relaxed Fit Fine-knit cardigan",
    sex="Men",
    category="Cardigans",
    original_price=159.99,
    current_price=99.99,
    description="Relaxed-fit cardigan in fine-knit cotton with a V-neck, buttons down the front and ribbing around the neckline, cuffs and hem.",
    additional_description="Cotton 100%",
    available_sizes="'XS':5, 'M':5, 'L':7",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F6e%2F67%2F6e675457ceb94e9bacefcafcdd13fa3f5614d698.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Ffc%2Ff0%2Ffcf0a7b545d4c06f23c3f86779e5652367d92ac7.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F66%2F16%2F6616a74e4ee5449dc98e34139d122a56f8d5d991.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Mike Regular Cardigan",
    sex="Men",
    category="Cardigans",
    original_price=199.99,
    current_price=49.99,
    description="A regular-fit single-breasted knit cardigan made from soft cotton and recycled polyester yarn. This go-to piece has a ribbed collar, six front buttons, mock-ribbed edges and sleeves, and all-over knitted detailing.",
    additional_description="Cotton 60%, Polyester 40%",
    available_sizes="'S':5, 'L':5, 'XXL':7",
    img_url="https://lp.weekday.com/app003prod?set=quality%5B79%5D%2Csource%5B%2Fde%2Fdd%2Fdedd525e2b81a838b378a21a6196697ece5adb34.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp.weekday.com/app003prod?set=quality%5B79%5D%2Csource%5B%2Fd5%2F8f%2Fd58f443488f39e31dedadd17a1e092376bc80a52.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp.weekday.com/app003prod?set=quality%5B79%5D%2Csource%5B%2F39%2Fbe%2F39be4552b697cf549d24f00208d3b8db6ef80dca.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Wrap Cardigan",
    sex="Women",
    category="Cardigans",
    original_price=249.99,
    current_price=189.99,
    description="Knitted wrap cardigan secured with a self-tie detail at the side. RECYCLED POLYESTER Ribbed cuffs and hem Size recommendation: This style runs large. We recommend ordering a size down from your usual size.",
    additional_description="Polyester 52%, Acrylic 38%, Wool 8%, Elastane 2%",
    available_sizes="'XS':3, 'S':5, 'M':8, 'L':5, 'XL':6, 'XXL':7",
    img_url="https://lp.stories.com/app005prod?set=quality%5B79%5D%2Csource%5B%2F93%2F4d%2F934d5c8fb36cb713062d2c944d28dd2732a74522.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp.stories.com/app005prod?set=quality%5B79%5D%2Csource%5B%2F2f%2Fe5%2F2fe5327daaf933ed8a4a5c67a2995ec47621bd91.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp.stories.com/app005prod?set=quality%5B79%5D%2Csource%5B%2F64%2Fe4%2F64e4e4d360b5597f2bdaf7bdeb807c9d97d5169b.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Oversized instarsia knit cardigan",
    sex="Women",
    category="Cardigans",
    original_price=209.99,
    current_price=139.99,
    description="An intarsia knit button up cardigan featuring a V-neck, ribbed trims and an extra button to adjust the waistline. Features a black and off-white abstract pattern.",
    additional_description="Cotton 100%",
    available_sizes="'M':8, 'L':5, 'XL':6, 'XXL':7",
    img_url="https://lp.monki.com/app002prod?set=quality%5B79%5D%2Csource%5B%2F65%2Fdf%2F65dfced774cd1ae4aa9d82e44d626f65c5be98a0.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp.monki.com/app002prod?set=quality%5B79%5D%2Csource%5B%2F59%2F1d%2F591d5216a0ea65b3f07216bd8aaca627b85ab06e.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp.monki.com/app002prod?set=quality%5B79%5D%2Csource%5B%2Fc7%2F21%2Fc721fa73e4364a63476d5f709c9b83a9c4b6656d.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Oversized mohair-blend cardigan",
    sex="Women",
    category="Cardigans",
    original_price=239.99,
    current_price=179.99,
    description="Oversized cardigan in a soft, fluffy knit containing mohair and merino wool. V-shaped opening, buttons down the front, low dropped shoulders and long sleeves. Ribbing around the neckline, down the button band and at the cuffs and hem.",
    additional_description="Wool 33%, Mohair 32%, Polyamide 32%, Elastane 3%",
    available_sizes="'XS':8, 'M':5, 'L':6, 'XXL':7",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Ffa%2F1c%2Ffa1cc353cf5101a6f8aa930eac84172ee4d4a390.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fe0%2Fc4%2Fe0c42622e298523e2532272350ae5d9c85448e32.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F9f%2F40%2F9f401067687b1ef38a345e07903fdc7133c57f1c.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Lightweight puffer jacket",
    sex="Men",
    category="Jackets",
    original_price=139.99,
    current_price=99.99,
    description="Lightweight puffer jacket in woven fabric with a hood and discreet zip down the front with a chin guard. Pockets in the side seams with a concealed zip, and narrow elastication at the cuffs and hem. Unlined.",
    additional_description="Polyester 100%",
    available_sizes="'XS':8, 'S':7, 'M':5, 'L':6, 'XL':8, 'XXL':7",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fd6%2F48%2Fd648135c33fe511484b9ccaf178847ac45ffdd59.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fc1%2F16%2Fc1169fa74e3a94e8e83207f1c12ee06412d77819.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F25%2F4c%2F254cbc2d70bbee9aa6351cdcab2d878d16c4d904.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Regular Fit jacket",
    sex="Men",
    category="Jackets",
    original_price=339.99,
    current_price=299.99,
    description="Short jacket with a collar and buttons down the front. Regular fit with long sleeves and buttoned cuffs, a yoke at the front and back, flap chest pockets and an inner pocket. Lined.",
    additional_description="Polyester 100%",
    available_sizes="'XS':5, 'M':6, 'XXL':7",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F56%2F7a%2F567a23f77fcd0c46ad2e6e151e3f987d49e6d86e.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5Bmen_jacketscoats_jackets%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Ffa%2Fd2%2Ffad225733667b10f9384a0794620f0360c0919ed.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5Bmen_jacketscoats_jackets%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F79%2F3d%2F793dd0e30862dcbd7aa8b4d936689c17843b2afc.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5Bmen_jacketscoats_jackets%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Bomber jacket",
    sex="Men",
    category="Jackets",
    original_price=219.99,
    current_price=169.99,
    description="Lightweight bomber jacket in woven fabric with a ribbed stand-up collar and zip down the front. Side pockets with a concealed press-stud, and an inner pocket with a press-stud. Wide ribbing at the cuffs and hem. Lined.",
    additional_description="Polyester 100%",
    available_sizes="'M':5, 'L':6, 'XL':7",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F04%2Fc3%2F04c37ffd9e5105aed6a5a910fc571f362cb343d4.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F4b%2Fd0%2F4bd02893911f9285d6fb76d5a135848c72cbfecc.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fd0%2F51%2Fd0510399e082276a3d6fe057e322df0f83024f38.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Cropped denim jacket",
    sex="Women",
    category="Jackets",
    original_price=259.99,
    current_price=129.99,
    description="Cropped jacket in sturdy cotton denim with a collar, metal buttons down the front and a yoke at the back. Dropped shoulders, long, wide sleeves with buttoned cuffs, and flap chest pockets with a button. Asymmetric hem at the front. Slightly longer at the back.",
    additional_description="Cotton 100%",
    available_sizes="'XS':6, 'S':7, 'M':5, 'L':6, 'XL':7, 'XXL':8",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F77%2F35%2F773546e66fa7fdf55f4fb01b5e3ff70d5f2ad7fb.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Ff3%2F11%2Ff311e47a9d8db6a086bbdeafa090ffd59182b57d.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fdd%2F44%2Fdd449b4c4aeb45160ba4349760e8d8d088035ccc.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Tie-belt denim jacket",
    sex="Women",
    category="Jackets",
    original_price=229.99,
    current_price=79.99,
    description="Jacket in rigid cotton denim with a collar, metal buttons down the front and a yoke at the front and back. Dropped shoulders, long sleeves, flap chest pockets and open front pockets. Wide, detachable tie belt at the waist and a single back vent.",
    additional_description="Cotton 100%",
    available_sizes="'XS':6, 'XL':7, 'XXL':8",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F98%2F42%2F9842651883261c2c11d9e0c0fcd6ac8e807cc953.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F4a%2Fe5%2F4ae523b38872e3fa4a78537352290260ca355c2f.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fbb%2Ff3%2Fbbf31df422c5ba5a93d7a648ef86d2eaafcda345.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Cargo Pocket Drawcord Jacket",
    sex="Women",
    category="Jackets",
    original_price=289.99,
    current_price=199.99,
    description="Cargo pocket drawcord jacket crafted from cotton accented with two large chest cargo pockets, two front flap pockets, a drawstring waist and a front placket concealing a zip and snap button closure and a classic turn-down collar. Finished with adjustable cuffs with snap button fixtures and topstitch detailing.",
    additional_description="Cotton 100%",
    available_sizes="'S':6, 'M':7, 'L':8",
    img_url="https://lp.stories.com/app005prod?set=quality%5B79%5D%2Csource%5B%2F25%2F97%2F2597b482a72282191487428e07255cb3dc2f937e.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp.stories.com/app005prod?set=quality%5B79%5D%2Csource%5B%2F24%2F69%2F24694ce0aeab9a46a5f9ff338ef32a8fa6927f79.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp.stories.com/app005prod?set=quality%5B79%5D%2Csource%5B%2Fdf%2F6f%2Fdf6f9c927bd43ee325c2cc7fd1106840d0e5ee7f.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Wool-blend coat",
    sex="Men",
    category="Coats",
    original_price=689.99,
    current_price=549.99,
    description="Coat in a soft, felted wool blend with notch lapels and buttons down the front. Long sleeves with decorative buttons at the cuffs. Flap front pockets, two inner pockets and a single back vent. Twill lining.",
    additional_description="Polyester 67%, Wool 33%",
    available_sizes="'XS':6, 'S':6, 'M':7, 'L':8, 'XL':6, 'XXL':3",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fd5%2F8f%2Fd58f54e821cd6fbc9cf8ac61f7a84150478c2c57.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fd8%2Fe5%2Fd8e58d4261f81dbbca201123eab1e425eb649d37.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Ff5%2F58%2Ff558d14462ae0ad63f3fdbdfef9882d4bdf2a4fe.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Essentials No 1: THE COAT",
    sex="Men",
    category="Coats",
    original_price=589.99,
    current_price=449.99,
    description="Coat in a felted wool blend with a refined twill texture, soft to the touch and super durable. Clean cut with a current, single-breasted silhouette, designed to fall just above the knee, and a relaxed fit for a loose silhouette. Notch lapels, a diagonal welt pocket at each side and a single back vent. A contemporary classic throughout the season. Lined.",
    additional_description="Wool 70%, Polyester 27%, Other fibres 3%",
    available_sizes="'S':7, 'M':8, 'XL':6, 'XXL':3",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Ff9%2F19%2Ff9191a086ac429c42b1e5379787c45fff590cd68.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F17%2Fbb%2F17bb19ce44ae3150163ec93fe258e035397c280e.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fcd%2F77%2Fcd771ac73d584175818e6dc6a9ac738b469d1f70.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Wool Pea Coat",
    sex="Men",
    category="Coats",
    original_price=789.99,
    current_price=649.99,
    description="Double-breasted pea coat in a recycled wool blend from Italy. Styled with two welt pockets at chest, two front pockets with flaps and two inner pockets. This pea coat has a straight fit with slightly dropped shoulders.",
    additional_description="Wool 70%, Polyester 27%, Other fibres 3%",
    available_sizes="'XS':7, 'S':8, 'M':6, 'XXL':3",
    img_url="https://lp.arket.com/app006prod?set=quality%5B79%5D%2Csource%5B%2F2f%2F54%2F2f547bac983787736b1dd874270acf870d6ce002.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp.arket.com/app006prod?set=quality%5B79%5D%2Csource%5B%2F9f%2F64%2F9f647a3f3f11be82b41d5c1a967d56596fb4cf58.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp.arket.com/app006prod?set=quality%5B79%5D%2Csource%5B%2F83%2F5a%2F835ad22dc2568c9313f75d459d22fbce13e1344a.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Double-breasted trenchcoat",
    sex="Women",
    category="Coats",
    original_price=689.99,
    current_price=449.99,
    description="Knee-length, double-breasted trenchcoat in a cotton weave. Notch lapels, a storm flap, buttons at the front and a detachable tie belt at the waist. Long sleeves with a decorative tab at the cuffs, diagonal welt pockets at the front and a single back vent. Lined.",
    additional_description="Cotton 100%",
    available_sizes="'XS':7, 'S':8, 'M':6, 'L':5, 'XL':6, 'XXL':3",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F88%2Fa3%2F88a33955f5b9f7e4918fc4de70308c3bb64907ba.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F4e%2F87%2F4e8726fccd6bff167506c61de3062bc5a9b6bdda.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fb9%2F94%2Fb99402eeed5bdc2cbf9f817ee891d1a750437870.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Tie-belt coat",
    sex="Women",
    category="Coats",
    original_price=489.99,
    current_price=349.99,
    description="Calf-length coat in twill. Loose fit with wide notch lapels and a detachable tie belt at the waist. Long raglan sleeves, welt front pockets and a straight-cut hem with a single back vent. Unlined.",
    additional_description="Polyester 82%, Viscose 16%, Elastane 2%",
    available_sizes="'XS':7, 'M':8, 'XL':3",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F30%2Fde%2F30de7dc54bc99809f71aefb7865abeef8db70bae.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F97%2Fbd%2F97bd7f18a9dbe95a49e4ad105448c7a30e08f57d.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fc2%2F68%2Fc2687e7db754d7a85bcffdeaef6f24367e9cd14b.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Classic double-breasted coat",
    sex="Women",
    category="Coats",
    original_price=789.99,
    current_price=549.99,
    description="Classic tailoring at its best, this double breasted elegant coat in wool blend with side pockets is sure to keep you warm and chic all winter long. Regular fit. Midi length. Regular shoulder. Notch lapel. Double breasted design. Slanted front pockets. Fully lined. Made with recycled polyester.",
    additional_description="Polyester 70%, Wool 20%, Other fibres 10%",
    available_sizes="'M':7, 'L':8, 'XXL':3",
    img_url="https://lp.monki.com/app002prod?set=quality%5B79%5D%2Csource%5B%2F40%2F35%2F403590a9d0931f26e2dc84b9329b38969050a89d.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp.monki.com/app002prod?set=quality%5B79%5D%2Csource%5B%2F80%2Fe9%2F80e9246581b244a8954cd787c1ea1670a70900d3.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp.monki.com/app002prod?set=quality%5B79%5D%2Csource%5B%2Ff0%2Ff9%2Ff0f94575a50234024f6d81af02c23362cd37986c.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Regular Fit Wool jumper",
    sex="Men",
    category="Jumpers",
    original_price=189.99,
    current_price=149.99,
    description="Regular-fit jumper in soft, fine-knit wool with a round, rib-trimmed neckline and ribbing at the cuffs and hem.",
    additional_description="Wool 100%",
    available_sizes="'XS':7, 'S':6, 'M':7, 'L':8, 'XL':6, 'XXL':3",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F81%2F14%2F81146ddd9c1e2f5ed32e8937ee86bb0b86e5443a.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F3f%2F0c%2F3f0cc418b34c4ef67e229b8866acf18bdab9d4f3.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fe5%2F4d%2Fe54d504dff45dbba0bb9b9ba0fd2974f09efe87e.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Relaxed Fit Jacquard-knit jumper",
    sex="Men",
    category="Jumpers",
    original_price=149.99,
    current_price=79.99,
    description="Relaxed-fit jumper in a soft cotton jacquard knit with a round, rib-trimmed neckline, dropped shoulders, long sleeves and wide ribbing at the cuffs and hem.",
    additional_description="Cotton 100%",
    available_sizes="'S':6, 'M':7, 'L':8, 'XL':6, 'XXL':3",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F77%2F18%2F77184231446cc3335ae69e6c72b52649590e25d0.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fac%2Fe0%2Face0abca7e4c4f8bce2d85a471e1e223036d8e86.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F6b%2F7d%2F6b7d2bac974baa919ea96e19b4ce4cacb4742e70.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Slim Fit Cashmere-blend jumper",
    sex="Men",
    category="Jumpers",
    original_price=199.99,
    current_price=129.99,
    description="Slim-fit jumper in a soft, fine-knit cotton and cashmere blend with a round neckline, long sleeves and ribbing around the neckline, cuffs and hem.",
    additional_description="Cotton 85%, Cashmere 15%",
    available_sizes="'XS':7, 'S':8, 'L':6, 'XXL':3",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fed%2F6b%2Fed6b5835f3709fa638dcc690eb889203f50c3fe4.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F31%2F48%2F31484b64f4b483fd13f5945d2ae1e9d91544446c.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F3d%2Fd9%2F3dd91114affd48556d29fa8e70ce852e35f9ba62.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Cotton Jumper",
    sex="Women",
    category="Jumpers",
    original_price=169.99,
    current_price=119.99,
    description="Jumper styled with a V-neck and a wide open collar. Made of organic cotton and knitted in a Milano rib. Slit at side seams.",
    additional_description="Cotton 100%",
    available_sizes="'XS':7, 'S':8, 'M':6, 'L':6, 'XL':8, 'XXL':3",
    img_url="https://lp.arket.com/app006prod?set=quality%5B79%5D%2Csource%5B%2F45%2F46%2F45469d7a4a42a9ddbafe83d65efc44df2d7a34cc.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp.arket.com/app006prod?set=quality%5B79%5D%2Csource%5B%2F10%2F41%2F10415c051af07eb8481d0af70b80655d38a441f9.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp.arket.com/app006prod?set=quality%5B79%5D%2Csource%5B%2Fb8%2Fb1%2Fb8b1d338da548c0d7734b337960ec32f33633763.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Pointelle-knit cotton jumper",
    sex="Women",
    category="Jumpers",
    original_price=189.99,
    current_price=139.99,
    description="Jumper in soft, pointelle-knit cotton with a crocheted look. Loose fit with a ribbed collar and V-shaped opening at the front. Dropped shoulders, long sleeves and scalloped edges at the cuffs and hem.",
    additional_description="Cotton 100%",
    available_sizes="'XS':6, 'M':6, 'L':8, 'XXL':3",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F55%2F1f%2F551fc6ced7228c76812251095297dcee8c99ce9f.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F80%2F9a%2F809acaef00172dfe62f0b4dc46d38c9604e3d77e.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F4f%2Fea%2F4fea42060f21a080227cee35be6eaca446c7d1f9.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Boxy jumper",
    sex="Women",
    category="Jumpers",
    original_price=129.99,
    current_price=59.99,
    description="Boxy-style jumper in soft jersey. Relaxed fit with a wide neckline, dropped shoulders and long, wide sleeves.",
    additional_description="Cotton 68%, Polyester 32%",
    available_sizes="'XS':6, 'S':6, 'M':8, 'XL':3",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F29%2F15%2F29151454d797a98eb7652aaa00548d17db26e5a6.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F4e%2Fa9%2F4ea939061d4fe0cf895efdf2509cc2b478ca20f0.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F27%2F3b%2F273bb17770e830adca6a4b72bbbaf485ccb7490f.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Slim Fit Cotton polo-neck top",
    sex="Men",
    category="Turtlenecks",
    original_price=129.99,
    current_price=99.99,
    description="Slim-fit top in soft cotton jersey with a polo neck and long sleeves.",
    additional_description="Cotton 95%, Elastane 5%",
    available_sizes="'XS':6, 'S':6, 'M':8, 'L':6, 'XL':3, 'XXL':8",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F25%2F6a%2F256af38da9f871f75fbb4c21655631ec3a19afe7.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F80%2Fbc%2F80bceb854b737fd3be5cd04389da21059b4b1caa.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F0f%2F80%2F0f80ccb1a8bd3b3ffc672c32b96753ccb4394cd5.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Slim Fit Fine-knit polo-neck jumper",
    sex="Men",
    category="Turtlenecks",
    original_price=159.99,
    current_price=129.99,
    description="Jumper in soft, fine-knit cotton with a ribbed polo neck, long sleeves and ribbing at the cuffs and hem.",
    additional_description="Cotton 100%",
    available_sizes="'XS':8, 'S':6, 'M':3, 'XXL':8",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F97%2F6c%2F976cf7f928b2c6ed99a58e386b98cd986dd03a94.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F51%2Fc2%2F51c24583186c6877482417ea1214355774f846fc.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fd9%2Fa5%2Fd9a52a1ac455eb617c33d931d1487ce7cb25e9ec.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Relaxed Fit Wool polo-neck jumper",
    sex="Men",
    category="Turtlenecks",
    original_price=149.99,
    current_price=109.99,
    description="Relaxed-fit polo-neck jumper knitted in soft wool with long sleeves and ribbing at the cuffs and hem.",
    additional_description="Wool 100%",
    available_sizes="'M':8, 'L':6, 'XL':3, 'XXL':8",
    img_url="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F25%2F67%2F2567354636408668833de8ba9d4e5f9d5769fde5.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2F4f%2Fef%2F4fef9c4f8b10c4808b011b60085b9d97670a1727.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp2.hm.com/hmgoepprod?set=quality%5B79%5D%2Csource%5B%2Fdb%2Fb3%2Fdbb34d5dfb7044d8a0c624010c327957a9bf5844.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Cropped turtleneck knit",
    sex="Women",
    category="Turtlenecks",
    original_price=149.99,
    current_price=109.99,
    description="A cropped turtleneck sweater with drop shoulders, ribbed cuffs and a chunky knit. Oversized fit. Cropped. Chunky knit. Made with recycled polyester.",
    additional_description="Polyester 64%, Acrylic 30%, Wool 6%",
    available_sizes="'XS':7, 'S':8, 'M':8, 'L':6, 'XL':3, 'XXL':8",
    img_url="https://lp.monki.com/app002prod?set=quality%5B79%5D%2Csource%5B%2Fcc%2F33%2Fcc33ebeddcb841875e8a5cf1f5f290a9e5716879.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp.monki.com/app002prod?set=quality%5B79%5D%2Csource%5B%2Fc0%2F7b%2Fc07b9b8deb18dc3c9deefc795d0d15e55b8f5eaf.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp.monki.com/app002prod?set=quality%5B79%5D%2Csource%5B%2F25%2F4f%2F254f1d1433535ed7b4e4c0672a683c54cb6ca58e.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Oversized Wool Knit Turtleneck",
    sex="Women",
    category="Turtlenecks",
    original_price=199.99,
    current_price=149.99,
    description="Oversized plain wool knit turtleneck with long sleeves and ribbed neck, hemline and cuffs.",
    additional_description="Wool 55%, Cotton 42%, Polyester 2%, Elastane 1%",
    available_sizes="'XS':8, 'M':6, 'L':3, 'XL':8",
    img_url="https://lp.stories.com/app005prod?set=quality%5B79%5D%2Csource%5B%2Fbb%2F2b%2Fbb2ba9036e92d7bc6c81b150c08bf9e1f005a750.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp.stories.com/app005prod?set=quality%5B79%5D%2Csource%5B%2F59%2F74%2F5974fed7f93d52faab2dcd837e83ec4c14926131.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp.stories.com/app005prod?set=quality%5B79%5D%2Csource%5B%2F7d%2F2e%2F7d2eee184ae57ec9fdb6f0f4639634db43ba7316.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

new_product = Product(
    name="Knitted turtleneck sweater",
    sex="Women",
    category="Turtlenecks",
    original_price=179.99,
    current_price=119.99,
    description="Ur new go-to turtleneck sweater? Yup! A stretchy and super cosy knit sweater featuring a ribbed low turtleneck, drop shoulders, ribbed hem details and a soft knitted texture.Regular fit. Ribbed hems. Drop shoulders. Made with recycled polyester.",
    additional_description="Polyester 90%, Wool 8%, Elastane 2%",
    available_sizes="'M':8, 'L':6, 'XL':3, 'XXL':8",
    img_url="https://lp.monki.com/app002prod?set=quality%5B79%5D%2Csource%5B%2Ffb%2F96%2Ffb964b23b19de92de0365ac3e9dab0f03a33fdd9.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url2="https://lp.monki.com/app002prod?set=quality%5B79%5D%2Csource%5B%2F42%2F6c%2F426c7a66f073f1206a36a84257249faa1998138d.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    img_url3="https://lp.monki.com/app002prod?set=quality%5B79%5D%2Csource%5B%2Fcf%2Ff4%2Fcff4dd18ea0f2bee7762942792c78c5d16142875.jpg%5D%2Corigin%5Bdam%5D%2Ccategory%5B%5D%2Ctype%5BLOOKBOOK%5D%2Cres%5Bm%5D%2Chmver%5B1%5D%2Ctarget%5Bhm.com%5D&call=url[file:/product/fullscreen]",
    date=datetime.datetime.now()
)
db.session.add(new_product)
db.session.commit()

