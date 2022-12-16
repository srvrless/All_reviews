from flask import flash, redirect, url_for, render_template, Blueprint
from flask_login import login_user, login_required, logout_user

from app import db
from app.forms import RegisterForm, LoginForm
from app.models import User,bcrypt


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
