from functools import wraps

from flask import Blueprint, redirect, url_for, flash, request, render_template
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from flaskdash.authentication.forms import LoginForm
from flaskdash.models import User
from flaskdash.login import login_manager

api = Blueprint("api", __name__, template_folder="templates")


@api.route("/")
@api.route("/index")
@login_required
def index():
    print (current_user)
    return render_template("index.html")