from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from  wtforms.validators import DataRequired, Email, EqualTo
import email_validator

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтверждение пароля', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')