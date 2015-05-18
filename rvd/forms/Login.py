from wtforms import fields, validators, ValidationError
from flask_babel import lazy_gettext as ___
from flask_wtf import Form
from rvd.models import session, User
from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound
import bcrypt


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
            alleged_user = session.query(User).filter(and_(User.email == self.login.data)).one()
            password = str(field.data)
            stored_pwd = str(alleged_user.password)
            stored_salt = str(alleged_user.password_salt)

            # try to hash PWD with our salt. Does it match result in DB?
            hashed_pwd = bcrypt.hashpw(password, stored_salt)

            if stored_pwd != hashed_pwd:
                print "NOPE"
                raise ValidationError("Wrong password")
        except NoResultFound:
            raise ValidationError("Could not find user")
        self.user = alleged_user