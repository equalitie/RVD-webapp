from wtforms import fields, validators
from flask_babel import lazy_gettext as ___
from flask_wtf import Form
from lib.models.User import User


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
        user = User({'id': 0})

        if self.login.data != "demo@demo.com" or field.data != "demo":
            raise validators.ValidationError(___('Try demo@demo.com/demo'))

        self.user = user