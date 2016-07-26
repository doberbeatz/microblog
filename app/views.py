from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash

from app import app, db, lm
from .forms import LoginForm, RegisterForm
from .models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=user.posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        user = User.query.filter_by(email=form.email.data).first()
        if user is None and not user.check_password_hash(form.password.data):
            flash('Invalid email or password. Try again')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register Page
    """
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            user = User(username=form.username.data,
                        email=form.email.data,
                        password=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            flash('Thanks for registering')
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('User "%s" is exists' % form.email.data)
    return render_template('register.html',
                           title='Sign In',
                           form=form)


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    g.user = current_user
