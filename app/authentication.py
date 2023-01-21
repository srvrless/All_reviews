import os
from authlib.integrations.flask_client import OAuth
from flask import flash, redirect, url_for, render_template, Blueprint, session, Flask
from flask_login import login_user
from wtforms import ValidationError

from app import db
from app.forms import RegisterForm, RegisterContinueForm, LoginForm
from app.models import User, bcrypt
from dotenv import load_dotenv

load_dotenv()

auth = Blueprint("auth", __name__)

app = Flask(__name__)
oauth = OAuth(app)
flow = oauth.register(
    name='google',
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'email profile'},
    fetch_token='https://oauth2.googleapis.com/token',
    server_metadata_url=f'https://accounts.google.com/.well-known/openid-configuration',
)


@auth.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)  # after create user instant login
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
            if bcrypt.check_password_hash(user.password_hash, form.password.data):  # Checking for passwords
                login_user(user)
                flash(f'You are logged in', category='success')
                return redirect(url_for('main.home_page'))
        flash(f'There was an error with login a user: Wrong username or password', category='danger')
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with login a user: {err_msg}', category='danger')
    return render_template('public/login.html', form=form)


@auth.route('/register_google', methods=['GET', 'POST'])
def register_google():
    user = dict(session).get('profile', None)
    # You would add a check here and usethe user id or something to fetch
    # the other data for that user/check if they exist
    if not user:
        google = oauth.create_client('google')  # create the google oauth client
        redirect_uri = url_for('auth.authorize_google', _external=True)
        return google.authorize_redirect(redirect_uri)
    return redirect('/logout')


@auth.route('/login_google', methods=['GET', 'POST'])
def login_google():
    user = dict(session).get('profile', None)
    # You would add a check here and usethe user id or something to fetch
    # the other data for that user/check if they exist

    if not user:
        google = oauth.create_client('google')  # create the google oauth client
        redirect_uri = url_for('auth.authorize_google', _external=True)
        return google.authorize_redirect(redirect_uri)
    return redirect('/logout')


@auth.route('/authorize_google', methods=['GET', 'POST'])
def authorize_google():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  #
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    # user = db.session.query(User)
    username = dict(session)['profile']['name']
    # You would add a check here and usethe user id or something to fetch
    # the other data for that user/check if they exist
    user = db.session.query(User).filter_by(username=username).first()
    if user:
        return redirect('/login_google_user')
    return redirect('/create_google_user')


@auth.route('/login_google_user', methods=['GET', 'POST'])
def login_google_user():
    username = dict(session)['profile']['name']
    user = db.session.query(User).filter_by(username=username).first()
    if user:
        login_user(user)
        flash(f'You are logged in', category='success')
        return redirect(url_for('main.home_page'))
    flash(f'There was an error with login a user: Wrong username or password', category='danger')


@auth.route('/create_google_user', methods=['GET', 'POST'])
def create_google_user():
    email = dict(session)['profile']['email']
    username = dict(session)['profile']['name']
    print(email)
    form = RegisterContinueForm()

    if form.validate_on_submit():
        user = db.session.query(User).filter_by(username=username).first()
        if user:
            raise ValidationError('Google account is already exist!')

        user_google_create = User(username=username,
                                  email_address=email,
                                  password=form.password1.data)
        db.session.add(user_google_create)
        db.session.commit()
        login_user(user_google_create)
        flash(f"Account created successfully! You are now logged in as {user_google_create.username}",
              category='success')
        return redirect(url_for('main.home_page'))
    return render_template('public/continue_register.html', form=form)


@auth.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/all_reviews')
