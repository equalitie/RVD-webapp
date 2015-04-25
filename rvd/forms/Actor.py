from wtforms import fields, validators
from flask_babel import lazy_gettext as ___  # the lazy_gettext aliased to ___ is for internationalization
from flask_wtf import Form


class ActorForm(Form):

    name = fields.StringField(
        validators=[validators.required()], description={
            'placeholder': ___('Name'),
        }
    )

    # why is there an age field is we are asking for birth_date just after?
    # I have omitted age for now
    #
    # age = fields.SelectField(label=___("Age"))
    birth_date = fields.DateField(format='%Y-%m-%d', description={
        'placeholder': ___('YYYY-MM-DD')
    })

    telephone_country_code = fields.IntegerField(___('Country Code'), description={'placeholder': ___('31')})
    telephone_area_code = fields.IntegerField(___('Area Code/Exchange'), description={'placeholder': ___('06')})
    telephone_number = fields.StringField(___('Number'), [validators.required()], description={
        'placeholder': ___('123-4567')
    })

    address = fields.StringField('Address', validators=[validators.required()], description={
        'placeholder': ___("12 42nd Ave. Springfield, NY, USA")
    })

    #  multiple choices take a list of tuples, set in the view directly
    organisations = fields.SelectMultipleField(default=['1', '3'])
    profession = fields.SelectMultipleField()
    location = fields.SelectMultipleField()

    gender = fields.RadioField(___('Gender'), validators=[validators.required()], choices=[
        ('M', ___('Male')), ('F', ___('Female'))]
    )

    is_activist = fields.BooleanField(label=___('Is activist'))
    activist_info = fields.TextAreaField()

    #  validate individual fields (custom) with methods called validate_<field_name>
    def validate_name(self, field):
        field_data = field.data
        name_parts = field_data.split(' ')
        if len(name_parts) < 2:
            raise validators.ValidationError(___("Please enter full name."))