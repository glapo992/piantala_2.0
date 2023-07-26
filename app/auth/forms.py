from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import Users


class LoginForm(FlaskForm):
    username    = StringField  ('Username', validators=[DataRequired(),Length(min=0, max=64)])
    password    = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField ('Ricordami')
    submit      = SubmitField  ('Accedi')

class RegistrationForm(FlaskForm):
    username  = StringField  ('Username',         validators=[DataRequired(), Length(min=0, max=64)])
    email     = EmailField   ('email',            validators=[DataRequired(), Email(), Length(min=0, max=64)])
    password  = PasswordField('Password',         validators=[DataRequired()])
    password2 = PasswordField('Conferma Password', validators=[DataRequired(), EqualTo('password')])
    submit    = SubmitField  ('Registrati adesso')

    # custom validators named "validate_<name_field>" are automaticcaly called by WTForms ad validators in the respective field
    def validate_username(self, username):
        """ search for another user with the same username in the db """
        user = Users.query.filter_by(username= username.data).first()
        if user is not None:
            raise ValidationError('username gia in uso')  # message flashed in case the validation fail
        
    def validate_email(self, email):
        """ search for another user with the same email in the db """
        user = Users.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('email già utilizzatta')
