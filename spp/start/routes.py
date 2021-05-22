from flask import render_template
from flask.helpers import url_for
from flask_login import current_user, login_user
from werkzeug.utils import redirect
from spp.start import bp
from spp.start.forms import LoginForm
from spp.models import User


@bp.route('/')
def index():
    return render_template("index.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("/"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return "login failed"
        login_user(user)
        return "login succeeded"
    return render_template("login.html", title="Login", form=form)
