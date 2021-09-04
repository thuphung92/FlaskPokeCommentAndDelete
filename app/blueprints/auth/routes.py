from flask import render_template, request, redirect, url_for,flash
from .forms import RegisterForm, LoginForm, EditProfileForm
from.models import User
from flask_login import login_user, logout_user, current_user, login_required
from . import bp as auth

@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "icon":int(form.icon.data),
                "password": form.password.data
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
        except:
            flash('There was an unexpected error', 'danger')
            return render_template('auth/register.html.j2',form=form)
        # Give the user some feedback that says registered successfully 
        flash('Registered Successfully','success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html.j2',form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email=form.email.data.lower()
        password=form.password.data
        user = User.query.filter_by(email=email).first()
        if user is not None and user.check_hashed_password(password):
            login_user(user)
            # Give user feedback of success
            flash('Logged in Successfully', 'success')
            return redirect(url_for('main.index'))
        else:
            # Give user feedback of failure
            flash('Invalid Email/Password', 'danger')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html.j2', form=form)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user is not None:
        logout_user()
        flash("You've been logged out",'warning')
        return redirect(url_for('auth.login'))

@auth.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
            #get info
        new_user_dict={
            "first_name": form.first_name.data.title(),
            "last_name": form.last_name.data.title(),
            "email": form.email.data.lower(),
            "icon": int(form.icon.data) if int(form.icon.data) !=9000 else current_user.icon,
            "password": form.password.data
        }
        user=User.query.filter_by(email=form.email.data.lower()).first()
        if user and current_user.email != user.email:
            flash('Email already in use','danger')
            return redirect(url_for('auth.edit_profile'))
            #create & save new user
        try:
            current_user.from_dict(new_user_dict)
            flash('Profile Updated Successfully','success')
            return redirect(url_for('main.index'))
        except:
            flash('Unexpected error', 'danger')
            return redirect('auth.edit_profile')
    return render_template('auth/register.html.j2', form=form)