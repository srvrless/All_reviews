import os
import pathlib
import requests
import google.auth.transport.requests

from flask import flash, redirect, url_for, render_template, Blueprint, abort, session, request
from flask_login import login_user, login_required, logout_user
from app import db
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from app.forms import RegisterForm, LoginForm
from app.models import User, bcrypt
from pip._vendor import cachecontrol

auth = Blueprint("auth", __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('main.home_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('public/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash(f'You are logged in', category='success')
                return redirect(url_for('main.home_page'))
        flash(f'There was an error with login a user: Wrong username or password', category='danger')
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with login a user: {err_msg}', category='danger')
    return render_template('public/login.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login_page'))


#
#
#
#
#
# GOOGLE_CLIENT_ID = "<Add your own unique Google Client Id from the client_secret.json here>"
# client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")
#
# flow = Flow.from_client_secrets_file(
#     client_secrets_file=client_secrets_file,
#     scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email",
#             "openid"],
#     redirect_uri="http://localhost/callback"
# )
#
#
# def login_is_required(function):
#     def wrapper(*args, **kwargs):
#         if "google_id" not in session:
#             return abort(401)  # Authorization required
#         else:
#             return function()
#
#     return wrapper
#
#
# @auth.route("/login_google")
# def login_google():
#     authorization_url, state = flow.authorization_url()
#     session["state"] = state
#     return redirect(authorization_url)
#
#
# @auth.route("/callback_google")
# def callback_goole():
#     flow.fetch_token(authorization_response=request.url)
#
#     if not session["state"] == request.args["state"]:
#         abort(500)  # State does not match!
#
#     credentials = flow.credentials
#     request_session = requests.session()
#     cached_session = cachecontrol.CacheControl(request_session)
#     token_request = google.auth.transport.requests.Request(session=cached_session)
#
#     id_info = id_token.verify_oauth2_token(
#         id_token=credentials._id_token,
#         request=token_request,
#         audience=GOOGLE_CLIENT_ID
#     )
#
#     session["google_id"] = id_info.get("sub")
#     session["name"] = id_info.get("name")
#     return redirect("/protected_area")
#
#
# @auth.route("/logout")
# def logout():
#     session.clear()
#     return redirect("/")
#
#
# @auth.route("/")
# def index():
#     return "Hello World <a href='/login'><button>Login</button></a>"
#
#
# @auth.route("/protected_area")
# @login_is_required
# def protected_area():
#     return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"
