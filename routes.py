import stripe
from flask import render_template, redirect, url_for, request, flash, session
from forms import LoginForm, RegisterForm, PasswordForm
from bs4 import BeautifulSoup
from flask_login import login_user, current_user, logout_user
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from redmail import outlook
from itsdangerous import SignatureExpired
from sqlalchemy import desc
from sqlalchemy import or_, and_
from models import User, Product, Discount, Order, Order_Details, Newsletter, Review
from __init__ import app, db, login_manager, url_serializer
import os
from dotenv import load_dotenv

load_dotenv()

outlook.username = os.getenv('EMAIL_USERNAME')
outlook.password = os.getenv('EMAIL_PASSWORD')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def show_main_page():
    """Show main page"""
    # Show only 8 newest products on the main page
    products = Product.query.order_by(desc(Product.date)).limit(8).all()
    return render_template("index.html", products=products)


@app.route('/product/<int:product_id>', methods=["GET", "POST"])
def view_product(product_id):
    """Show a specific product to the user"""
    # Fetch all reviews from a specific product
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.posted_on.desc()).all()
    # Get specific product
    requested_product = Product.query.get(product_id)
    # Fetch similar products associated with the same category
    similar_products = Product.query.filter_by(category=requested_product.category).all()

    # If a user adds product to the cart
    if request.method == 'POST':
        # If 'cart' doesn't exist in a session, then create it and assign variables
        if 'cart' not in session:
            session['cart'] = []
            session['cart'].append({'product_id': requested_product.id, 'size': request.form["size"],
                                    "quantity": int(request.form["quantity"])})
        # If 'cart' does exist in a session and isn't empty
        elif session['cart']:
            # Go through each element in session['cart']
            for element in session['cart']:
                # If an element already exists in session['cart'], then just add quantity to it
                if element['product_id'] == requested_product.id and element['size'] == request.form["size"]:
                    element['quantity'] += int(request.form["quantity"])
                    break
                # If it's the last element in a loop and matching element hasn't been found, then add new element to the list
                elif element == session['cart'][-1]:
                    session['cart'].append({'product_id': requested_product.id, 'size': request.form["size"],
                                            "quantity": int(request.form["quantity"])})
                    break
        # If cart exists in session and is empty
        else:
            session['cart'].append({'product_id': requested_product.id, 'size': request.form["size"],
                                    "quantity": int(request.form["quantity"])})
        session.modified = True
        return render_template("product.html", product=requested_product, reviews=reviews,
                               similar_products=similar_products)
    else:
        return render_template("product.html", product=requested_product, reviews=reviews,
                               similar_products=similar_products)


@app.route('/leave-a-review/<int:product_id>', methods=["POST"])
def leave_a_review(product_id):
    """Post a review about a specific product"""
    # Get variables from the form
    rating = request.form['rating']
    review = request.form['review']
    name = request.form['name']
    email = request.form['email']
    # Add new entry to the database
    new_review = Review(
        rating=rating,
        text=review,
        name=name,
        email=email,
        product_id=product_id,
        posted_on=datetime.datetime.now(),
    )
    db.session.add(new_review)
    db.session.commit()
    return redirect(url_for('view_product', product_id=product_id))


@app.route('/login', methods=["GET", "POST"])
def login():
    """A page where user can log in"""
    form = LoginForm()
    # If user is already authenticated, then go to the main page
    if current_user.is_authenticated:
        return redirect(url_for('show_main_page'))
    # If form has been validated
    if form.validate_on_submit():
        # Get variables from the form
        email = form.email.data
        password = form.password.data
        # Check if user already exists in a database
        user = User.query.filter_by(email=email).first()
        # If an email doesn't exist in a database, then show appropriate message
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        # If user hasn't confirmed his email address yet
        elif not user.confirmed:
            flash("Seems like you haven't confirmed your email address yet. If your link has already expired, "
                  "please register once again.")
            return redirect(url_for('login'))
        # If passwords don't match
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        # In other cases login user
        else:
            login_user(user)
            return redirect(url_for('show_main_page'))
    return render_template("login.html", form=form)


@app.route('/register', methods=["GET", "POST"])
def register():
    """A page where user can register"""
    form = RegisterForm()
    # If user is already logged in, then go to the main page
    if current_user.is_authenticated:
        return redirect(url_for('show_main_page'))
    # If a form has been successfully validated
    if form.validate_on_submit():
        user_record = User.query.filter_by(email=form.email.data).first()
        # If user already exists and already confirmed his email
        if user_record is not None and user_record.confirmed:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        # If user doesn't exist, then create a record
        elif user_record is None:
            # Encrypt a password in a database
            hash_and_salted_password = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            # Add a new entry
            new_user = User(
                name=form.name.data,
                surname=form.surname.data,
                email=form.email.data,
                password=hash_and_salted_password,
                address=form.address.data,
                postal_code=form.postal_code.data,
                city=form.city.data,
                country=form.country.data,
                confirmed=False,
                registered_on=datetime.datetime.now()
            )
            db.session.add(new_user)
        # If user already exists, but didn't confirm his email, then update his entry
        elif user_record is not None:
            hash_and_salted_password = generate_password_hash(
                form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            user_record.name = form.name.data
            user_record.surname = form.surname.data
            user_record.email = form.email.data
            user_record.password = hash_and_salted_password
            user_record.address = form.address.data
            user_record.postal_code = form.postal_code.data
            user_record.city = form.city.data
            user_record.country = form.country.data
            user_record.confirmed = False
            user_record.registered_on = datetime.datetime.now()

        # Commit changes to the database
        db.session.commit()
        # Show a message
        message = "Please check your email and confirm your registration"
        # Send an email to the user to confirm his registration
        email = form.email.data
        token = url_serializer.dumps(email, salt="register-confirm")
        link = url_for("confirm_registration", token=token, _external=True)
        HTMLFile = open("templates/register_mail.html", "r")
        index = HTMLFile.read()
        S = BeautifulSoup(index, 'html.parser')
        outlook.send(
            receivers=[email],
            subject="Registration confirmation",
            html=f"""{S.body.prettify()}""",
            body_params={
                'link': link,
            }
        )
        return render_template("register_info.html", message=message)

    return render_template("register.html", form=form)


@app.route('/confirm-registration/<string:token>')
def confirm_registration(token):
    """Confirms user registration"""
    try:
        # Check if a token hasn't expired
        email = url_serializer.loads(token, salt="register-confirm", max_age=3600)
        user_record = User.query.filter_by(email=email).first()
        # If user hasn't confirmed his registration yet, then update an entry in a database
        if not user_record.confirmed:
            user_record.confirmed = True
            user_record.confirmed_on = datetime.datetime.now()
            db.session.commit()
            message = "You've successfully confirmed your registration."
            login_user(user_record)
        # If user has already confirmed his registration
        else:
            message = "Seems like you've already confirmed your registration."
    except SignatureExpired:
        message = "Seems like the link has expired."
    return render_template("register_info.html", message=message)


@app.route('/logout')
def logout():
    """Logs user out"""
    # If user isn't logged in, then go to the main page
    if not current_user.is_authenticated:
        return redirect(url_for('show_main_page'))
    logout_user()
    return redirect(url_for('show_main_page'))


@app.route('/cart')
def cart():
    """Shows a shopping cart to the user"""
    products = Product.query.all()
    return render_template("cart.html", products=products)


@app.route('/change-quantity/<int:element_id>', methods=["POST"])
def change_quantity(element_id):
    """Changes quantity in a cart"""
    if request.method == "POST":
        element = session['cart'][element_id]
        element["quantity"] = int(request.form["quantity"])
        session.modified = True
    return redirect(url_for('cart'))


@app.route('/remove-item/<int:element_id>', methods=["POST"])
def remove_item(element_id):
    """Removes an item from the cart"""
    if request.method == "POST":
        del session['cart'][element_id]
        session.modified = True
    return redirect(url_for('cart'))


@app.route('/check-discount', methods=["POST"])
def check_discount():
    """Checks if discount exists in a database"""
    discounts = Discount.query.all()
    if request.method == "POST":
        # Go through all discounts in a database
        for discount in discounts:
            # If a discount is in a database and hasn't expired
            if discount.name == request.form["discount"] and discount.expiration_date >= datetime.date.today():
                # If there is no 'discount' in a session, then create it
                if "discount" not in session:
                    session['discount'] = []
                # Add a discount to the session['discount']
                session['discount'].append({'name': discount.name, 'percent': discount.percent_sale, 'id': discount.id})
                break
            # If a discount doesn't exist, then show a message
            else:
                flash("That discount doesn't exist or it has expired.")
                break
    return redirect(url_for('cart'))


@app.route('/remove-discount', methods=["POST"])
def remove_discount():
    """Removes a discount from the shopping cart"""
    if request.method == "POST":
        session.pop("discount")
    return redirect(url_for('cart'))


@app.route('/create-checkout-session', methods=["POST"])
def create_checkout_session():
    """Creates a checkout session"""
    line_items = []
    products = Product.query.all()
    # If there is no 'cart' in a session, then show a message
    if "cart" not in session:
        flash("Please add products to your cart.")
        return redirect(url_for('cart'))
    session["order"] = session["cart"]
    session["total_price"] = 0.0
    # If user isn't logged in, then show a message
    if not current_user.is_authenticated:
        flash("You have to be logged in to buy products.")
        return redirect(url_for('cart'))
    # Check if user added discount to his cart
    if "discount" in session:
        product_discount = session['discount'][0]['name']
    else:
        product_discount = False
    # Go through each element in session['cart'] and assign variables
    for element in session["cart"]:
        product_name = products[element["product_id"] - 1].name
        product_quantity = element["quantity"]
        product_price = products[element['product_id'] - 1].current_price
        product_img = products[element['product_id'] - 1].img_url
        product_size = element["size"]
        line_items.append({
            'price_data': {
                'currency': 'pln',
                'product_data': {
                    'name': product_name + f" [{product_size}]",
                    'images': [product_img],
                },
                'unit_amount': int(product_price * 100),
            },
            'quantity': product_quantity,
        })
        session["total_price"] = session["total_price"] + (product_price * product_quantity)
    # Add free shipping to the cart
    line_items.append({
        'price_data': {
            'currency': 'pln',
            'product_data': {
                'name': "Shipping",
                'images': ["https://www.apsfulfillment.com/wp-content/uploads/2017/03/APS_28.jpg"],
            },
            'unit_amount': 0,
        },
        'quantity': 1,
    })
    # If total price of items is equal to 0, then show user a message
    if session["total_price"] == 0:
        flash("Please add items to your cart.")
        return redirect(url_for('cart'))
    # If discount exists, then include it in the checkout session
    if product_discount:
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            discounts=[{
                'coupon': product_discount,
            }],
            success_url=url_for('thanks', _external=True),
            cancel_url=url_for('cart', _external=True)
        )
    # If discount doesn't exist, then don't include it in the checkout session
    else:
        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            success_url=url_for('thanks', _external=True),
            cancel_url=url_for('cart', _external=True)
        )
    return redirect(checkout_session.url, code=303)


@app.route('/thanks')
def thanks():
    """Shows user 'thank you' page after placing an order and sends an email confirmation"""
    try:
        # Initialize variables
        products = Product.query.all()
        order_list = []
        discount_name = None
        discount_percent = 0
        discount_amount = 0
        discount_id = None
        # Get information about discount
        if 'discount' in session:
            discount_id = session['discount'][0]['id']
            discount_amount = (session['discount'][0]['percent'] / 100) * session["total_price"]
        # Create a new order in the database
        new_order = Order(
            user_id=current_user.id,
            discount_id=discount_id,
            order_date=datetime.datetime.now(),
            total=session["total_price"] - discount_amount
        )
        db.session.add(new_order)
        db.session.commit()
        # Go through each product in session['order'] and assign variables
        for element in session["order"]:
            product_name = products[element["product_id"] - 1].name
            product_quantity = element["quantity"]
            product_price = products[element['product_id'] - 1].current_price
            product_img = products[element['product_id'] - 1].img_url
            product_size = element["size"]
            order_list.append({
                'name': product_name,
                'image': product_img,
                'price': product_price,
                'quantity': product_quantity,
                'size': product_size
            })
            # Add a new product entry to the orders_details table
            new_order_details = Order_Details(
                order_id=new_order.id,
                product_id=element["product_id"],
                product_size=element["size"],
                product_quantity=element["quantity"],
                subtotal=products[element['product_id'] - 1].current_price * element["quantity"]
            )
            db.session.add(new_order_details)
            db.session.commit()
        # Open the html file
        HTMLFile = open("templates/order_mail.html", "r")
        # Read the file
        index = HTMLFile.read()
        # Create a BeautifulSoup object and specify the parser
        S = BeautifulSoup(index, 'html.parser')
        # Delete cart from the session
        del session['cart']
        # Delete discount from the session, if it already exists
        if 'discount' in session:
            discount_name = session['discount'][0]['name']
            discount_percent = session['discount'][0]['percent']
            del session['discount']
        session.modified = True
        # Send an email to the user
        outlook.send(
            receivers=[current_user.email],
            subject="Order confirmation",
            html=f"""{S.body.prettify()}""",
            body_params={
                'current_user': current_user.name,
                'order_list': order_list,
                'discount_name': discount_name,
                'discount_percent': discount_percent,
                'order_id': new_order.id,
            }
        )
    except:
        return redirect(url_for('show_main_page'))
    return render_template("order_confirmation.html")


@app.route('/my-orders')
def my_orders():
    """Shows user his placed orders"""
    # If user isn't logged in, then redirect him to the main page
    if not current_user.is_authenticated:
        return redirect(url_for('show_main_page'))
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return render_template("orders.html", orders=orders)


@app.route('/order/<int:order_id>')
def order(order_id):
    """Shows user a specific order"""
    # If user isn't logged in, then redirect him to the main page
    if not current_user.is_authenticated:
        return redirect(url_for('show_main_page'))
    order = Order.query.filter_by(id=order_id).first()
    # If user isn't the one who placed an order, then redirect him to the main page
    if current_user.id != order.user_id:
        return redirect(url_for('show_main_page'))
    order_products = Order_Details.query.filter_by(order_id=order_id).all()
    products = Product.query.all()
    discounts = Discount.query.all()
    return render_template("order.html", discounts=discounts, order=order, order_products=order_products,
                           products=products)


@app.route('/sign-to-newsletter', methods=["POST"])
def sign_to_newsletter():
    """Signs user up to the newsletter"""
    email = request.form["email"]
    newsletter_record = Newsletter.query.filter_by(email=email).first()
    # If user has signed up to the newsletter
    if newsletter_record is not None:
        # If user hasn't confirmed his subscription
        if not newsletter_record.confirmed:
            message = "Please check your email and confirm your newsletter subscription"
            # Update an existing entry in the database and send confirmation link on email
            newsletter_record.registered_on = datetime.datetime.now()
            newsletter_record.name = request.form["name"]
            db.session.commit()
            token = url_serializer.dumps(email, salt="newsletter-confirm")
            link = url_for("confirm_newsletter", token=token, _external=True)
            HTMLFile = open("templates/newsletter_mail.html", "r")
            index = HTMLFile.read()
            S = BeautifulSoup(index, 'html.parser')
            outlook.send(
                receivers=[email],
                subject="Newsletter confirmation",
                html=f"""{S.body.prettify()}""",
                body_params={
                    'link': link,
                }
            )
        else:
            message = "You've already signed up with that email"
    # If user hasn't already signed up to the newsletter
    else:
        message = "Please check your email and confirm your newsletter subscription"
        # Add new entry in the database and send confirmation link on email
        new_subscriber = Newsletter(
            name=request.form["name"],
            email=email,
            confirmed=False,
            registered_on=datetime.datetime.now()
        )
        db.session.add(new_subscriber)
        db.session.commit()
        token = url_serializer.dumps(email, salt="newsletter-confirm")
        link = url_for("confirm_newsletter", token=token, _external=True)
        HTMLFile = open("templates/newsletter_mail.html", "r")
        index = HTMLFile.read()
        S = BeautifulSoup(index, 'html.parser')
        outlook.send(
            receivers=[email],
            subject="Newsletter confirmation",
            html=f"""{S.body.prettify()}""",
            body_params={
                'link': link,
            }
        )
    return render_template("newsletter_info.html", message=message)


@app.route('/confirm-newsletter/<string:token>')
def confirm_newsletter(token):
    """Confirms user subscription to the newsletter"""
    try:
        # Check if a token hasn't expired
        email = url_serializer.loads(token, salt="newsletter-confirm", max_age=3600)
        newsletter_record = Newsletter.query.filter_by(email=email).first()
        # If user hasn't confirmed his subscription yet
        if not newsletter_record.confirmed:
            newsletter_record.confirmed = True
            newsletter_record.confirmed_on = datetime.datetime.now()
            db.session.commit()
            message = "You've successfully signed up to the newsletter."
        # If user has already signed up to the newsletter
        else:
            message = "Seems like you've already signed up to the newsletter."
    # If signature has already expired
    except SignatureExpired:
        message = "Seems like the link has expired."
    return render_template("newsletter_info.html", message=message)


@app.route('/search', methods=["GET", "POST"])
def search():
    """Searches for specific products"""
    # Initialize some starting variables
    sizes_list = []
    gender_list = []
    all_genders = ["Men", "Women"]
    page = request.args.get('page', 1, type=int)
    all_products = Product.query
    sort_by = None
    search_query = request.args.get("q", None)
    initial_results = all_products.filter(or_(Product.name.like("%" + search_query + "%"),
                                              Product.category.like("%" + search_query + "%"),
                                              Product.sex.like(search_query)))

    # If number of matching items is more than 0, set min and max value of price
    if initial_results.count() > 0:
        general_min_price = min(product.current_price for product in initial_results)
        general_max_price = max(product.current_price for product in initial_results)
        min_price = min(product.current_price for product in initial_results)
        max_price = max(product.current_price for product in initial_results)
    # If number of matching items is equal to 0, then set min and max price to 0
    else:
        general_min_price = 0
        general_max_price = 0
        min_price = 0
        max_price = 0
    # Go through each product in results and fetch all available sizes
    for product in initial_results:
        temp_sizes = product.available_sizes.split("'")[1::2]
        for size in temp_sizes:
            if size not in sizes_list:
                sizes_list.append(size)

    # Reassign variables to empty lists
    all_sizes = sizes_list
    sizes_list = []
    sizes_quantity = []
    gender_quantity = []

    # Get parameters from the link, if they are available
    if request.args.get("min_price") is not None:
        min_price = float(request.args.get("min_price"))
        max_price = float(request.args.get("max_price"))
        sizes_list = request.args.getlist("sizes_list")
        gender_list = request.args.getlist("gender_list")

    # If user has pressed filter button, then get all variables and go back to the first page
    if request.method == "POST":
        min_price = float(request.form["min-price"])
        max_price = float(request.form["max-price"])
        sizes_list = request.form.getlist("size")
        gender_list = request.form.getlist("sex")
        if page != 1:
            page = 1

    # Switch variables if min price is greater than max
    if min_price > max_price:
        min_price, max_price = max_price, min_price

    # Count quantity of products available in each size
    for size in all_sizes:
        sizes_quantity.append(Product.query.filter(and_(or_(Product.name.like("%" + search_query + "%"),
                                                            Product.category.like("%" + search_query + "%"),
                                                            Product.sex.like(search_query)),
                                                        Product.current_price >= min_price,
                                                        Product.current_price <= max_price,
                                                        or_(*[Product.sex.like(gender) for gender in gender_list]),
                                                        Product.available_sizes.like("%" + f"'{size}'" + "%"))).count())

    # Count quantity of products available for men and women
    for gender in all_genders:
        gender_quantity.append(Product.query.filter(and_(or_(Product.name.like("%" + search_query + "%"),
                                                             Product.category.like("%" + search_query + "%"),
                                                             Product.sex.like(search_query)),
                                                         Product.current_price >= min_price,
                                                         Product.current_price <= max_price,
                                                         or_(*[Product.available_sizes.like("%" + size + "%") for size
                                                               in sizes_list]),
                                                         Product.sex.like(gender))).count())

    # Get all products after filtering
    filtered_products = all_products.filter(or_(Product.name.like("%" + search_query + "%"),
                                                Product.category.like("%" + search_query + "%"),
                                                Product.sex.like(search_query)),
                                            Product.current_price >= min_price,
                                            Product.current_price <= max_price,
                                            or_(*[Product.available_sizes.like("%" + size + "%") for size in
                                                  sizes_list]),
                                            or_(*[Product.sex.like(gender) for gender in gender_list]))

    # If user has chosen sorting, then order products accordingly
    if request.args.get("sort_by") is not None:
        if request.args.get("sort_by") == "latest":
            sort_by = "latest"
            filtered_products = filtered_products.order_by(Product.date.desc()).paginate(page=page, per_page=6)
        elif request.args.get("sort_by") == "most_expensive":
            sort_by = "most_expensive"
            filtered_products = filtered_products.order_by(Product.current_price.desc()).paginate(page=page, per_page=6)
        elif request.args.get("sort_by") == "least_expensive":
            sort_by = "least_expensive"
            filtered_products = filtered_products.order_by(Product.current_price.asc()).paginate(page=page, per_page=6)
    else:
        filtered_products = filtered_products.paginate(page=page, per_page=6)

    return render_template("search.html", general_min_price=general_min_price, general_max_price=general_max_price,
                           min_price=min_price, max_price=max_price, sizes=all_sizes, sizes_list=sizes_list,
                           gender_list=gender_list,
                           products=filtered_products, all_products=all_products, sizes_quantity=sizes_quantity,
                           gender_quantity=gender_quantity,
                           search_query=search_query, sort_by=sort_by)


@app.route('/edit-profile', methods=["GET", "POST"])
def edit_profile():
    """Edits profile"""
    # If user isn't logged in, then go back to the main page
    if not current_user.is_authenticated:
        return redirect(url_for('show_main_page'))
    profile = User.query.get(current_user.id)
    # Auto fill a form with user's information
    edit_form = RegisterForm(
        name=profile.name,
        surname=profile.surname,
        email=profile.email,
        address=profile.address,
        postal_code=profile.postal_code,
        city=profile.city,
        country=profile.country,
    )
    edit_form.submit.label.text = "Edit profile"
    # Update user's profile if the form has successfully validated
    if edit_form.validate_on_submit():
        hash_and_salted_password = generate_password_hash(
            edit_form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        profile.name = edit_form.name.data
        profile.surname = edit_form.surname.data
        profile.email = edit_form.email.data
        profile.password = hash_and_salted_password
        profile.address = edit_form.address.data
        profile.postal_code = edit_form.postal_code.data
        profile.city = edit_form.city.data
        profile.country = edit_form.country.data
        db.session.commit()
        return redirect(url_for("edit_profile"))

    return render_template("edit_profile.html", form=edit_form)


@app.route('/restore-password', methods=["POST", "GET"])
def restore_password():
    """Restores user's password"""
    # If user is already logged in, then go back to the main page
    if current_user.is_authenticated:
        return redirect(url_for('show_main_page'))
    # If the form has been sent
    if request.method == "POST":
        email = request.form["email"]
        user = User.query.filter_by(email=email).first()
        # Display a message if user doesn't exist
        if user is None:
            flash("That email doesn't exist in our database.")
            return redirect(url_for("restore_password"))
        # Generate a link for the user to reset his password
        else:
            token = url_serializer.dumps(email, salt="password-restore")
            link = url_for("change_password", token=token, _external=True)
            HTMLFile = open("templates/password_mail.html", "r")
            index = HTMLFile.read()
            S = BeautifulSoup(index, 'html.parser')
            outlook.send(
                receivers=[email],
                subject="Restore your password",
                html=f"""{S.body.prettify()}""",
                body_params={
                    'link': link,
                }
            )
            flash("Check your email to restore password.")
            return redirect(url_for("restore_password"))
    return render_template("password_restore.html")


@app.route('/change-password/<string:token>', methods=["GET", "POST"])
def change_password(token):
    """Changes user's password"""
    password_form = PasswordForm()
    message = None
    try:
        # Check if signature hasn't expired
        email = url_serializer.loads(token, salt="password-restore", max_age=3600)
        user = User.query.filter_by(email=email).first()
        # Update user's password
        if password_form.validate_on_submit():
            hash_and_salted_password = generate_password_hash(
                password_form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            user.password = hash_and_salted_password
            db.session.commit()
            message = "You've successfully reset your password."
    # If signature has already expired
    except SignatureExpired:
        message = "Seems like the link has expired."
    return render_template("password_info.html", message=message, form=password_form)
