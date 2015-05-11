from wtforms import fields, validators
from flask_babel import lazy_gettext as ___
from flask_wtf import Form
from rvd.models import session, User
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound


class LoginForm(Form):
    user = None

    login = fields.StringField(
        validators=[validators.required(), validators.email()], description={
            'placeholder': ___('email'),
        }
    )
    password = fields.PasswordField(
        validators=[validators.required()], description={
            'placeholder': ___('password'),
        }
    )

    def validate_password(self, field):
        try:
            result = session.query(User).filter(and_(User.email == self.login.data, User.password == field.data)).one()
        except NoResultFound:
            result = None
        self.user = result