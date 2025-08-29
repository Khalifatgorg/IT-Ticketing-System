from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
email = StringField('Email', validators=[DataRequired(), Email()])
submit = SubmitField('Login')


class TicketForm(FlaskForm):
employee_id = StringField('Employee ID', validators=[DataRequired()])
employee_name = StringField('Employee Name', validators=[DataRequired()])
branch = StringField('Branch', validators=[DataRequired()])
branch_code = StringField('Branch Code', validators=[DataRequired()])
department = StringField('Department', validators=[DataRequired()])
issue_type = SelectField('Issue Type', choices=[('Hardware','Hardware'),('Software','Software'),('Network','Network')], validators=[DataRequired()])
description = TextAreaField('Issue Description', validators=[DataRequired()])
attachment = FileField('Attachment')
submit = SubmitField('Submit Ticket')


class AssignForm(FlaskForm):
admin_id = HiddenField('admin_id', validators=[DataRequired()])
submit = SubmitField('Assign')


class NotifyForm(FlaskForm):
content = TextAreaField('Content', validators=[DataRequired()])
submit = SubmitField('Post Notification')
