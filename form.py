from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, EmailField, DateField, RadioField, SelectField, SubmitField, IntegerField

from wtforms.validators import DataRequired, Length, equal_to, NumberRange
from flask_wtf.file import FileField, FileRequired
class RegisterForm(FlaskForm):
    profile_image = FileField("Upload File")
    email = EmailField("Enter Email", validators=[DataRequired()])
    birthday = DateField("Date of birth", validators=[DataRequired()])
    gender = RadioField("Gender", choices =["Male", "Female" ], validators=[DataRequired()])
    country = SelectField("Country", choices=["Georgia", "USA", "UK", "Russia"], validators=[DataRequired()])
    username = StringField("Enter username", validators=[DataRequired()])
    password = PasswordField("Enter password", validators=[DataRequired(), Length(min=8, max=64)])
    repeat_password = PasswordField("Repeat password", validators=[DataRequired(),
                                                                   equal_to("password", message="პაროლი და განმეორებითი პაროლი არ ემთხვევა.")])
    register = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Enter username", validators=[DataRequired()])
    password = PasswordField("Enter password", validators=[DataRequired(), Length(min=8, max=64)])

    login = SubmitField("Log in")


class AddFood(FlaskForm):
    image = FileField("Upload an image")
    name = StringField("Enter the name of the food", validators=[DataRequired()])
    description = StringField("Enter the description/recipe", validators=[DataRequired()])
    country = SelectField("Enter the city", choices=["Tbilisi", "Batumi", "Tusheti", "Kutaisi", "Rustavi", "Gori", "Zugdidi", "Poti", "Kobuleti", "Khashuri", "Samtredia", "Senaki", "Zestafoni", "Telavi", "Akhaltsikhe", "Ozurgeti", "Kaspi"], validators=[DataRequired()])
    address = StringField("Enter the address", validators=[DataRequired()])
    price = StringField("Enter the price", validators=[DataRequired()])
    register = SubmitField("Add")

class EditUserForm(FlaskForm):
    profile_image = FileField("Upload File")
    username = StringField("Enter username", validators=[DataRequired()])
    email = StringField("Enter email", validators=[DataRequired()])
    password = StringField("Enter password", validators=[DataRequired(), Length(min=8, max=64)])
    birthday = DateField("Date of birth", validators=[DataRequired()])

    save = SubmitField("ცვლილებების შენახვა")

class RatingForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit Rating')


class CommentForm(FlaskForm):
    comment = StringField("Leave a comment", validators=[DataRequired()])
    submit = SubmitField('Post a comment')