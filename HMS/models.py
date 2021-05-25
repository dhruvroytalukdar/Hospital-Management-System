from HMS import db, login_manager
import datetime
import uuid
from flask_login import UserMixin, current_user
from flask import redirect, url_for


@login_manager.user_loader
def load_user(doctor_id):
    return Doctor.query.get(doctor_id)

    # Represents a single doctor in the database
    # Doctor(email,first_name,last_name,image_file='if any',password)


class Doctor(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_file = db.Column(
        db.String(20), default='default.jpg', nullable=False)

    # One to many relationship between the appointment and doctors
    appointments = db.relationship('Appointment', backref="doctor", lazy=True)

    # Many to many relationship with the specialization table
    # Because a doctor can have many specialization and a single specialization can be of many doctors
    specializations = db.relationship(
        'Specialization', secondary='specialization_table', lazy="subquery", backref=db.backref('doctors', lazy=True))

    roles = db.Column(db.String(20), default="staff")

    def __repr__(self):
        return f"Doctor({self.first_name} {self.last_name})"


# Examples 'Cardiology' 'Neurology' 'Haematology'
# Specialization(name_of_specialization)


class Specialization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"Specialization({self.name})"


# Table to create the many to many relationship between two Relations
specialization_table = db.Table('specialization_table',
                                db.Column('doctor_id', db.Integer,
                                          db.ForeignKey('doctor.id'), primary_key=True),
                                db.Column('specialization_id', db.Integer,
                                          db.ForeignKey('specialization.id'), primary_key=True)
                                )

# Appointment table and stores each appointment by the user
# Appointment(patient_name,phone_number,date,time_id,problems,doctor_id)


def custom():
    return uuid.uuid4().hex


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(50), nullable=False,
                     unique=True, default=custom)
    patient_name = db.Column(db.String(60), nullable=False)
    phone_number = db.Column(db.String(10), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.date.today)
    problems = db.Column(db.Text, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey(
        'doctor.id'), nullable=False)
    time_id = db.Column(db.Integer, db.ForeignKey(
        'timeslots.id'), nullable=False)

    def __repr__(self):
        return f"Appointment for {self.patient_name} on {self.date}"

# Table to store the TimeSlots of appointments
# TimeSlots(hours,mins)


class Timeslots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hours = db.Column(db.Integer, nullable=False)
    mins = db.Column(db.Integer, nullable=False)
    appointments = db.relationship(
        'Appointment', backref="timeslot", lazy=True)

    def __repr__(self):
        return f"Time({self.hours}:{self.mins})"
