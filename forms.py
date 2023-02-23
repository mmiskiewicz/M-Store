from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    postal_code = StringField("Postal code", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    submit = SubmitField("Sign up")
