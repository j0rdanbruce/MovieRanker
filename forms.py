from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, EqualTo

class RegistrationForm(FlaskForm):
    fname = StringField("First Name", validators=[DataRequired()])
    lname = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password1 = PasswordField('Password', validators = [DataRequired()])
    password2 = PasswordField('Confirm Password', validators = [DataRequired(),EqualTo('password1')])
    submit = SubmitField('Register')

#might have to pip install email validator for this one
class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    #remember = BooleanField('Remember Me',validators= [DataRequired()])
    submit = SubmitField('Login')

class SearchMovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired()])
    search = SubmitField('Search Movie')

class ForumForm(FlaskForm):
    title = StringField('Forum Title', validators=[DataRequired()])
    body = StringField(validators=[DataRequired()])
    private = BooleanField('Private?')
    post = SubmitField('Post')

class CommentForm(FlaskForm):
    body = StringField('Write your heart out!', validators=[DataRequired()])
    comment = SubmitField('Comment')