from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from wtforms import validators


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     validators.Length(min=6, max=10,
                                                                       message="Password must be between 6 and 10 characters long.")
                                                     ])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(),
                                                                     validators.EqualTo('password',
                                                                                        message='Passwords must match.')
                                                                     ])
    address = StringField("Address", validators=[DataRequired()])
    postal_code = StringField("Postal code", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    country = StringField("Country", validators=[DataRequired()])
    submit = SubmitField("Sign up")


class PasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(),
                                                     validators.Length(min=6, max=10,
                                                                       message="Password must be between 6 and 10 characters long.")
                                                     ])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired(),
                                                                     validators.EqualTo('password',
                                                                                        message='Passwords must match.')
                                                                     ])
    submit = SubmitField("Reset Password")
