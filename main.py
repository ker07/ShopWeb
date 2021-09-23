from flask import render_template, redirect, url_for, flash, abort, session
from forms import LoginForm, RegisterForm, AddToCartForm, AddItemForm, EditCartItemForm, CheckForm, ResetPasswordForm, \
    ResetPasswordRequestForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from functools import wraps
from model import app, db, CartItem, User, Item, worker_list
from flask_migrate import Migrate
from mail import send_password_reset_mail
from chat import socketio
from dotenv import load_dotenv
import os

# create table in db (only at first time)
# db.create_all()

Migrate(app, db)
load_dotenv()

# server config
MAIL_SERVER = "smtp.googlemail.com"
MAIL_PORT = 587
MAIL_USE_TLS = 1
MAIL_USERNAME = "Shoppp Test"
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_ADDRESS = os.environ.get('MAIL_ADDRESS')

# LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id not in worker_list:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


# routes
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/itemlist/<int:page_number>")
def show_all_items(page_number):
    page = Item.query.paginate(page=page_number)
    return render_template("itemlist.html", page=page, current_user=current_user)


@app.route("/cart")
@login_required
def show_cart_item():
    form = CheckForm()
    user_id = current_user.id
    cart_item = CartItem.query.filter_by(buyer_id=user_id)
    if form.validate_on_submit():
        ##TODO:res1 = session.query(Account).filter(or_(Account.name=='哈哈', Account.gender=='男', Account.id==2)).all()
        pass
    return render_template("cart.html", all_cart_item=cart_item, current_user=current_user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()
        # Check if email exists and whether password is correct
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for("login"))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            session["name"] = user.name
            session["room_id"] = user.id
            return redirect(url_for('home'))

    return render_template("log_in.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        if User.query.filter_by(email=form.email.data).first():
            print(User.query.filter_by(email=form.email.data).first())
            # user already exists
            flash("You've already signed up with that email, try to log in!")
            return redirect(url_for("login"))

        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=10
        )

        new_user = User(
            email=form.email.data,
            password=hash_and_salted_password,
            name=form.name.data,
            sex=form.sex.data,
            birthday=form.birthday.data
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))

    return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('home'))


@app.route("/item/<int:item_id>", methods=["GET", "POST"])
def item(item_id):
    form = AddToCartForm()
    showed_item = Item.query.get(item_id)

    if form.validate_on_submit():
        _add_item = CartItem(
            item_id=item_id,
            quantity=form.quantity.data,
            item=showed_item.name,
            buyer_id=current_user.id,
        )

        db.session.add(_add_item)
        db.session.commit()

        return redirect(url_for("show_cart_item"))

    return render_template("item.html", item=showed_item, form=form, current_user=current_user)


@app.route("/edit-cart/<int:cartitem_id>", methods=["GET", "POST"])
@login_required
def edit_cart(cartitem_id):
    cart_item = CartItem.query.get(cartitem_id)
    edit_form = EditCartItemForm(
        quantity=cart_item.quantity
    )
    if edit_form.validate_on_submit():

        if edit_form.quantity == 0:
            # delete
            cart_item_to_be_deleted = CartItem.query.get(cartitem_id)
            db.session.delete(cart_item_to_be_deleted)
            db.session.commit()
            return redirect(url_for("show_cart_item"))

        else:
            cart_item.quantity = edit_form.quantity.data
            db.session.commit()
            return redirect(url_for("show_cart_item"))

    return render_template("edit_cart.html", item_id=cartitem_id, item=cart_item, form=edit_form)


@app.route("/delete/<int:item_in_cart_id>")
@login_required
def delete_item_in_cart(item_in_cart_id):
    item_in_cart_to_be_deleted = CartItem.query.get(item_in_cart_id)
    db.session.delete(item_in_cart_to_be_deleted)
    db.session.commit()
    return redirect(url_for("show_cart_item"))


@app.route("/add", methods=["GET", "POST"])
@login_required
@admin_only
def add_item():
    form = AddItemForm()

    if form.validate_on_submit():
        new_item = Item(
            name=form.name.data,
            price=form.price.data,
            stock=form.stock.data,
            category=form.category.data,
            color=form.color.data,
            start_selling_time=form.start_selling_time.data,
            stop_selling_time=form.stop_selling_time.data,
            size=form.size.data,
        )

        db.session.add(new_item)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("add.html", form=form, current_user=current_user)


@app.route('/reset_password_request', methods=["GET", "POST"])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_mail(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', form=form)


@app.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for("home"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


if __name__ == "__main__":
    socketio.run(
        app,
        host='localhost',
        port=5000,
        use_reloader=False,
        debug=False
    )
