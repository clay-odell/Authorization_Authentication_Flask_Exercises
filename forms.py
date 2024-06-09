from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Username is required, and must be no longer than 20 characters."), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(message="Password is required")])
    email = StringField('Email', validators=[DataRequired(), Length(max=50)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=30)])
    
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    
class FeedbackForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    content = StringField('Content', validators=[DataRequired()])