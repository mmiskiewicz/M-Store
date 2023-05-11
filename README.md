<h1 align="center">
  <img src=https://github.com/mmiskiewicz/M-Store/assets/32812860/1a1821e6-7b82-4e71-bd74-99109c56f8ef></img>
  </h1>

<h4 align="center">
E-commerce web app where you can purchase clothes.
  </h4>
  
  
  <h5 align="center">
  <img src=https://user-images.githubusercontent.com/32812860/228517917-fd65c2a0-f3b4-4f8d-8063-cfd84cc650d9.svg></img>
    <img src=https://forthebadge.com/images/badges/built-with-love.svg></img>
       </h5>

  
  <h5 align="center">
   <img src=https://img.shields.io/github/repo-size/mmiskiewicz/M-Store></img>
  <img src=https://img.shields.io/github/issues/mmiskiewicz/M-Store></img>
    </h5>
    
<p align="center">
  <a href="#tech-used">Tech</a> •
  <a href="#key-features">Key Features</a> •
  <a href="#installation">Installation</a> •
  <a href="#usage">Usage</a> •
  <a href="#payments">Payments</a> •
  <a href="#demo">Demo</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#acknowledgements">Acknowledgements</a>
</p>

 ## Tech used

1. Framewok
    + Flask
2. Database
    + SQLAlchemy
3. Payments
    + Stripe API
4. Forms
    + WTForms
5. Other
    + Passwords encrypted
    + Tokens
    + Pagination
    + Gravatar API
    + Bootstrap
    + HTML, CSS, JS

    
 ## Key Features
 - <a href="#signing-in">Signing in</a>
 - <a href="#signing-up">Signing up and confirming registration</a>
 - <a href="#editing-profile">Editing profile</a>
 - <a href="#searching-filtering-and-ordering-results">Searching, filtering and ordering results</a>
 - <a href="#showing-specific-and-related-products">Showing specific and related products</a>
 - <a href="#purchasing-products">Adding to shopping cart</a>
 - <a href="#changing-quantity-of-products">Changing quantity of items</a>
 - <a href="#writing-reviews">Writing reviews</a>
 - <a href="#adding-and-removing-discounts">Adding and removing discounts</a>
 - <a href="#purchasing-products">Purchasing products</a>
 - <a href="#signing-up-to-newsletter">Signing up to newsletter</a>
 - <a href="#restoring-password">Restoring passwords</a>
 - <a href="#purchasing-products">Showing order history</a>


 
## Installation

1. Clone the repository by `git clone https://github.com/mmiskiewicz/M-Store.git`.
2. Use the `pip install -r requirements.txt` command to install all of the Python modules and packages listed in `requirements.txt` file.
3. Create `.env` file located in `shop-website` folder and set up environment variables:

    + Initiate `SECURITY_KEY` and `SECURITY_PASSWORD_SALT` variables with any random string of your choice.
    + Create an account on Stripe and use your generated public and secret key in `STRIPE_PUBLIC_KEY` and `STRIPE_SECRET_KEY` variables. Make sure it says `pk_test` and `sk_test` respectively.
    + Ideally you'd want to put your outlook credentials for `EMAIL_USERNAME` and `EMAIL_PASSWORD` since code in `routes.py` is based around this email provider.
    + Assign `"sqlite:///shop.db"` to `SQLALCHEMY_DATABASE_URI` variable in order to use `shop.db` local database.
        - If you're using some type of cloud application hosting, you can create PostgreSQL file, so that your database won't get wiped every day. Because the app is based around SQLAlchemy, there's nothing you need to change in terms of code. You just need to set up PostgreSQL database and tell your cloud application hosting about it. Simply create new PostgreSQL database and assign its database URL to `SQLALCHEMY_DATABASE_URI`. Keep in mind that the URI should start with `postgresql://` instead of `postgres://`. SQLAlchemy used to accept both, but has removed support for the latter.
        
<h2 align="center"><img width=700px; src=https://user-images.githubusercontent.com/32812860/229126323-b215b888-c1eb-4827-9011-5d8d9aca740d.png></img></h2>

## Usage

`cd` into the project folder, type `python main.py` in your terminal and run your local server.

## Payments

The application uses Stripe API for payment purposes. In order to successfully authorize your payment, you need to use their <a href="https://stripe.com/docs/testing">test cards</a>. Here's how it works:
1. Provide Stripe test card number, such as `4242 4242 4242 4242`.
2. Use a valid future date, such as 12/34.
3. Use any three-digit CVC (four digits for American Express cards).
4. Use any value you like for other form fields.
<h1 align="center"><img src=https://b.stripecdn.com/docs-statics-srv/assets/test-card.c3f9b3d1a3e8caca3c9f4c9c481fd49c.jpg></img></h1>


## Demo

<p align="center">
<h3>Signing in</h3>
<img src=https://user-images.githubusercontent.com/32812860/228603756-a6e1443b-34cb-49f1-87d2-64b11ece9c30.gif></img>
<h3>Signing up</h3>
<img src=https://user-images.githubusercontent.com/32812860/228852369-68696929-11c9-4ef0-a074-14625207e3df.gif></img>
<h3>Editing profile</h3>
<img src=https://user-images.githubusercontent.com/32812860/228603496-83917906-8784-44c3-8131-b75c3db2f43e.gif></img>
<h3>Searching, filtering and ordering results</h3>
<img src=https://user-images.githubusercontent.com/32812860/228853898-88b745c5-3394-43fb-a7a8-7207708ab07b.gif></img>
<h3>Showing specific and related products</h3>
<img src=https://user-images.githubusercontent.com/32812860/228606724-ff4d5a60-a9d5-4af9-ba22-abc7973ca45c.gif></img>
<h3>Changing quantity of products</h3>
<img src=https://user-images.githubusercontent.com/32812860/228604133-b340e9a7-8032-4b2e-8972-f3c936764232.gif></img>
<h3>Writing reviews</h3>
<img src=https://user-images.githubusercontent.com/32812860/228604922-5510fe0b-ed85-4aa5-8c15-a79d1f6917c9.gif></img>
<h3>Adding and removing discounts</h3>
<img src=https://user-images.githubusercontent.com/32812860/228603341-00e4d5fd-359c-4d2b-adb3-882fccd3a01b.gif></img>
<h3>Purchasing products</h3>
<img src=https://user-images.githubusercontent.com/32812860/228603995-2539bc2d-ad34-43f2-aae5-c7fb66a9787b.gif></img>
<h3>Signing up to newsletter</h3>
<img src=https://user-images.githubusercontent.com/32812860/228613467-5b9b6c8a-861a-48cb-8512-b5deae122eb0.gif></img>
<h3>Restoring password</h3>
<img src=https://user-images.githubusercontent.com/32812860/228604561-7e69bfc6-2413-4e72-8d01-9f5d8eef26d1.gif></img>





</p>

## Contributing

1. Clone the repo and create a new branch `git checkout https://github.com/mmiskiewicz/M-Store -b <branch_name>`.
2. Make changes and test.
3. Submit Pull Request with description of changes.

## Acknowledgements

Theme designed by <a href="https://htmlcodex.com">HTML Codex</a>. Distributed by <a href="https://themewagon.com">ThemeWagon</a>.

