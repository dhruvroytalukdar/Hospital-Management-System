from HMS.models import *
from HMS.decorators import *
from flask_login import login_user, logout_user
from flask import render_template, redirect, url_for, flash
from HMS import app, bcrypt, db
from HMS.forms import *

# Route to delete a specialization
# Restricted to admins


@app.route('/delete/<variable>', methods=['GET'])
@requires_roles('admin')
def specializationDeleteView(variable):
    s = Specialization.query.filter_by(name=variable).first()
    s.doctors.clear()
    Specialization.query.filter_by(name=variable).delete()
    db.session.commit()
    flash('Specialization deleted successfully')
    return redirect(url_for('adminView'))


# Route to delete a doctor
# Restricted to admins


@app.route('/delete/doctor/<variable>', methods=['GET'])
@requires_roles('admin')
def doctorDeleteView(variable):
    print("Doctor", variable)
    doc = Doctor.query.filter_by(id=variable).first()
    doc.specializations.clear()
    Doctor.query.filter_by(id=variable).delete()
    db.session.commit()
    flash('Account deleted successfully')
    return redirect(url_for('adminView'))

# Home page
# Unrestricted


@app.route('/')
def home():
    return render_template('home.html', name="Dhruv Roy Talukdar")


# Route to register doctors
# Restricted to admins

@app.route('/admin/register/doctor', methods=['POST', 'GET'])
@requires_roles('admin')
def registerDoctorView():
    form = DocterRegistrationForm()
    # print(form.specializations.data)
    if form.validate_on_submit():
        doctor = Doctor.query.filter_by(email=form.email.data).first()

        # Check if the doctor with that name already exists
        if doctor is not None:
            flash(f'User with that email already exists please try another one')
            form = DocterRegistrationForm()
            return render_template('register.html', form=form, title='Register')
        password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')

        # Intialize doctor variable
        doctor = Doctor(email=form.email.data, password=password,
                        first_name=form.first_name.data, last_name=form.last_name.data)

        # Append all the selected specializations
        for sp in form.specializations.data:
            doctor.specializations.append(
                Specialization.query.filter_by(name=sp).first())

        # Append "General Medicine" by default
        doctor.specializations.append(
            Specialization.query.filter_by(name="General Medicine").first())

        doctor.roles = form.role.data

        # Create the doctor tuple in the database
        db.session.add(doctor)
        db.session.commit()

        # Return a flash message indicating successful creation of new doctor
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
    return redirect(url_for('home'))


def getSpecializations():
    li = Specialization.query.all()
    li.remove(Specialization.query.filter_by(name="General Medicine").first())
    return li


def getDoctors():
    docs = Doctor.query.all()
    return docs


@app.route('/admin', methods=['POST', 'GET'])
@requires_roles('admin')
def adminView():
    spform = CreateSpecializationForm()
    rolform = DoctorRoleForm()
    get_list = getSpecializations()
    doctor_list = getDoctors()
    if spform.validate_on_submit():
        name = spform.name.data
        print(f'name recieved {name}')
        sp = Specialization.query.filter_by(name=name).first()
        if sp is not None:
            flash('Sorry specialization with that name already exists')
        else:
            flash('New Specialization created')
            sp = Specialization(name=name)
            db.session.add(sp)
            db.session.commit()
            return redirect(url_for('adminView'))
    return render_template('admin.html', title="Admin Page", form=spform, list=get_list, doctors=doctor_list)
