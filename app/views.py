from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash
from sqlalchemy import or_
from datetime import datetime

from app import app, db, lm
from .forms import LoginForm, RegisterForm, EditForm, PostForm
from .models import User, Post
from .emails import follower_notification
from config import POSTS_PER_PAGE


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    """
    Index Page
    """
    form = PostForm()
    user = g.user
    page = 1
    if 'PAGE' in request.args and int(request.args['PAGE']) > 1:
        page = int(request.args['PAGE'])
    if request.method == 'POST' and form.validate_on_submit():
        post = Post(body=form.post.data, timestamp=datetime.utcnow(), author=user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!', 'success')
        return redirect(url_for('index'))
    posts = user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
    return render_template('index.html',
                           title='Home',
                           user=user,
                           form=form,
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login Page
    """
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password. Try again', 'danger')
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
        user = User.query.filter(or_(User.email == form.email.data, User.username == form.username.data)).first()
        if user is None:
            user = User(username=form.username.data,
                        email=form.email.data,
                        password=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            # Make the user follow himself
            db.session.add(user.follow(user))
            db.session.commit()
            flash('Thanks for registering', 'success')
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('User with same data is exists', 'danger')
    return render_template('register.html',
                           title='Sign In',
                           form=form)


@app.route('/profile/', defaults={'username': None})
@app.route('/profile/<username>')
@login_required
def profile(username):
    """
    Profile page
    :param username Just a Username
    """
    if username is None:
        username = g.user.username
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %s is not found.' % username, 'danger')
        redirect(url_for('index'))
    return render_template('profile.html',
                           user=user,
                           posts=user.posts)


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    form = EditForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and g.user.username != form.username.data:
            flash('Username "%s" is used by another user. Please type another' % form.username.data, 'danger')
            return redirect(url_for('profile_edit'))
        g.user.username = form.username.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been successfully saved', 'success')
        return redirect(url_for('profile_edit'))
    else:
        form.username.data = g.user.username
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)


@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %s  not found' % username, 'danger')
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t follow yourself', 'danger')
        return redirect(url_for('profile', username=username))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow %s.' % username, 'danger')
        return redirect(url_for('profile', username=username))
    db.session.add(u)
    db.session.commit()
    flash('You are now following %s!' % username, 'success')
    follower_notification(user, g.user)
    return redirect(url_for('profile', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User %s  not found' % username, 'danger')
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t unfollow yourself', 'danger')
        return redirect(url_for('profile', username=username))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow %s.' % username, 'danger')
        return redirect(url_for('profile', username=username))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following %s!' % username, 'success')
    return redirect(url_for('profile', username=username))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 400


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
