from flask_wtf import FlaskForm
from wtforms import widgets, StringField, PasswordField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from HMS.models import Specialization


def getSpecializations():
    li = Specialization.query.all()
    ans = []
    for sp in li:
        ans.append((sp.name, sp.name))
    print('returned list', ans)
    return ans


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class DocterRegistrationForm(FlaskForm):
    first_name = StringField('First Name',
                             validators=[DataRequired(), Length(max=20)])
    last_name = StringField('Last Name',
                            validators=[DataRequired(), Length(max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    role = SelectField(choices=[('admin', 'admin'), ('staff', 'staff')])
    specializations = MultiCheckboxField(
        'Select a specialization', choices=getSpecializations(), validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class CreateSpecializationForm(FlaskForm):
    name = StringField('Name of Specialization', validators=[DataRequired()])
    submit = SubmitField('Create')


class DoctorLoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class DoctorRoleForm(FlaskForm):
    role = SelectField(choices=[('admin', 'admin'), ('staff', 'staff')])
    submit = SubmitField('Change')
