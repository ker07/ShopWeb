from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, SelectField
from wtforms.validators import DataRequired, EqualTo, Email
from wtforms.fields.html5 import DateField, DateTimeLocalField

#WTForm
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log me in!")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_2 = PasswordField("Type in your password again", validators=[DataRequired(), EqualTo("password", message="Passwords must match")])
    name = StringField("Name", validators=[DataRequired()])
    sex = SelectField("Sex", choices=[("female", "Female"), ("male", "Male")])
    birthday = DateField("Birthday", validators=[DataRequired()])
    submit = SubmitField("Sign me up!")


class AddToCartForm(FlaskForm):
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    submit = SubmitField("Add to Cart")


class AddItemForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    stock = IntegerField("Stock", validators=[DataRequired()])
    category = SelectField("Category", choices=[("cloths", "Cloths"), ("pants", "Pants"), ("accessories", "Accessories"), ("underwear", "Underwear")], validators=[DataRequired()])
    color = SelectField("Color", choices=[("white", "White"), ("black", "Black"), ("red", "Red"), ("green", "Green"), ("blue", "Blue")], validators=[DataRequired()])
    size = SelectField("Size", choices=[("s", "S"), ("m", "M"), ("l", "L")], validators=[DataRequired()])
    start_selling_time = DateTimeLocalField("Time start selling", format="%Y-%m-%dT%H:%M")
    stop_selling_time = DateTimeLocalField("Time stop selling", format="%Y-%m-%dT%H:%M")
    submit = SubmitField("Add to item list!")


class EditCartItemForm(FlaskForm):
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    submit = SubmitField("Save Change")


class CheckForm(FlaskForm):
    quantity = IntegerField("Quantity", validators=[DataRequired()])
    submit = SubmitField("Pay the check")


class CommentForm(FlaskForm):
    text = StringField("Comment", validators=[DataRequired()])
    submit = SubmitField("Add comment to this item!")


class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Request Password Reset")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Request Password Reset")