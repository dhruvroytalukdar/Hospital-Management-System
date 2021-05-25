from HMS.models import *
from HMS.decorators import *
from flask_login import login_user, logout_user
from flask import render_template, redirect, url_for, flash
from HMS import app, bcrypt, db
from HMS.forms import *


@app.route('/')
def home():
    return render_template('home.html', name="Dhruv Roy Talukdar")


@app.route('/admin/register/doctor', methods=['POST', 'GET'])
@requires_roles('admin')
def registerDoctorView():
    form = DocterRegistrationForm()
    if form.validate_on_submit():
        doctor = Doctor.query.filter_by(email=form.email.data).first()
        if doctor is not None:
            flash(f'User with that email already exists please try another one')
            form = DocterRegistrationForm()
            return render_template('register.html', form=form, title='Register')
        password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        doctor = Doctor(email=form.email.data, password=password,
                        first_name=form.first_name.data, last_name=form.last_name.data)
        db.session.add(doctor)
        db.session.commit()
        flash(f'Account created for {doctor.email}', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form, title='Register')


@app.route('/admin/staff/login', methods=['POST', 'GET'])
@already_logged_in()
def doctorLoginView():
    form = DoctorLoginForm()
    if form.validate_on_submit():
        doctor = Doctor.query.filter_by(email=form.email.data).first()
        if doctor and bcrypt.check_password_hash(doctor.password, form.password.data):
            login_user(doctor, remember=False)
            return redirect(url_for('doctorView'))
        else:
            flash(f'Login unsuccessful.Invalid credentials')
    else:
        print('Not validated')
    return render_template('login.html', form=form, title="Login")


@app.route('/admin/staff/doctor')
@requires_roles('staff', 'admin')
def doctorView():
    return render_template('doctordashboard.html', title="Doctor DashBoard")


@app.route('/admin/logout')
def adminLogoutView():
    logout_user()
    return redirect(url_for('home', title="Home"))


@app.route('/admin')
@requires_roles('admin')
def adminView():
    return render_template('admin.html', title="Admin Page")
