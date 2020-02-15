from functools import wraps

from flask import Blueprint, redirect, url_for, flash, request, render_template
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse

from flaskdash.authentication.forms import LoginForm
from flaskdash.models import User
from flaskdash.login import login_manager

authentication = Blueprint("authentication", __name__, template_folder="templates")


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@login_manager.request_loader
def load_user_from_request(request):
    auth = request.authorization
    if not auth:
        return None
    user = User.query.filter_by(username=auth.username).first()
    if user is None:
        user = User.query.filter_by(email=auth.username).first()
    if not user or not user.check_password(auth.password):
        return None
    return user

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("authentication.login"))


def roles_required(role="ANY"):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            if current_user.role != role and role != "ANY":
                return login_manager.unauthorized()
            return func(*args, **kwargs)

        return decorated_view

    return wrapper


@authentication.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("api.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None:
            user = User.query.filter_by(email=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("authentication.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("api.index")
        return redirect(next_page)
    return render_template("login.html", form=form)


@authentication.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("authentication.login"))
