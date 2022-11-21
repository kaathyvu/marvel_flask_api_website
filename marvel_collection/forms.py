from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserSignUpForm(FlaskForm):
    email = StringField('*Email', validators=[DataRequired(), Email()])
    first_name = StringField('*First Name', validators=[DataRequired()])
    last_name = StringField('Last Name')
    password = PasswordField('*Password', validators=[DataRequired()])
    submit_button = SubmitField('Submit')

class UserSignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField('Submit')

class AddMarvelCharForm(FlaskForm):
    superhero_name = StringField('*Superhero Alias', validators=[DataRequired()])
    name = StringField('Character Name')
    description = StringField('Description')
    num_of_comics = StringField('Number of Comics Appeared In')
    superpower = StringField('*Superpower or Specialty', validators=[DataRequired()])
    user_token = StringField('User Token', validators=[DataRequired()])
    submit_button = SubmitField('Add Character')
