from flask import render_template
from flask.helpers import url_for
from flask_login import current_user, login_user
from flask_login.utils import login_required, logout_user
from werkzeug.utils import redirect
from spp.start import bp
from spp.start.forms import LoginForm, RegistrationForm
from spp.models import User
from spp import db


@bp.route('/')
def index():
    return render_template("index.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Logging in the user.
    -> Returns back to index if already authenticated
    -> loads again upon submitting
        -> logs in if appropriate, returns success
        -> return login page with a failed attempt mention otherwise
    """
    if current_user.is_authenticated:
        return redirect(url_for("start.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return render_template("login.html", title="Login", form=form, failedAttempt=True)
        login_user(user)
        return redirect(url_for("start.index")) 
    return render_template("login.html", title="Login", form=form)


@bp.route("/logout")
def logout():
    """
    Logs out the user.
    Brings user back to index.
    """
    logout_user()
    return redirect(url_for("start.index"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Register the user.
    """
    if current_user.is_authenticated:
        return redirect(url_for("start.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("start.login"))
    return render_template("register.html", title="Register", form=form)


@bp.route("/account")
@login_required
def account():
    return render_template("account.html")


@bp.route("/deleteaccount")
@login_required
def delete_account():
    User.query.filter(User.id == current_user.id).delete()
    db.session.commit()
    return redirect(url_for("start.index"))

@bp.route("/unauthorised")
def unauthorised():
    return render_template("unauthorised.html")
