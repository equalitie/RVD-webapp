from flask_babel import lazy_gettext as ___  # the lazy_gettext aliased to ___ is for internationalization

import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from wtforms_alchemy import ModelForm, ModelFieldList
from sqlalchemy_utils import PhoneNumberType, ChoiceType
from wtforms import fields, validators


engine = create_engine('sqlite:///:memory:')
Base = declarative_base(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Actor(Base):
    __tablename__ = 'actors'

    id = sa.Column(sa.BigInteger, autoincrement=True, primary_key=True)
    name = sa.Column(sa.Unicode(200), nullable=False, info={'description': ___('Name'), 'label': ___('Name')})
    dob = sa.Column(sa.Date, nullable=False, info={'description': ___('Name'), 'label': ___('Date of birth')})
    phone_number = sa.Column(PhoneNumberType(), info={
        'description': ___('+1 819 987-6543'), 'label': ___('Phone number')}
    )
    address = sa.Column(sa.Unicode(250), nullable=False, info={'description': ___('Address'), 'label': ___('Address')})

    # these 3 could/should probably be relationships
    organisation = sa.Column(ChoiceType([('1', '1')]), nullable=True)
    profession = sa.Column(ChoiceType([('1', '1')]), nullable=True)
    location = sa.Column(ChoiceType([('1', '1')]), nullable=True)

    gender = sa.Column(sa.Boolean, nullable=False, info={'description': ___('Gender'), 'label': ___('Gender')})
    is_activist = sa.Column(
        sa.Boolean, nullable=False, info={'description': ___('Is activist'), 'label': ___('Is activist')}
    )
    activist_info = sa.Column(
        sa.Text, nullable=True, info={'description': ___('Activist info'), 'label': ___('Activist info')}
    )


class ActorForm(ModelForm):

    class Meta:
        model = Actor

    # this is a bit shitty, but required if we want to have a proper order in the fields.
    # if you move/change fields, they HAVE to be added here, until this code is made better...
    __order = (
        'name', 'dob', 'phone_number', 'address', 'organisations',
        'profession', 'location', 'gender', 'is_activist', 'activist_info'
    )

    def __iter__(self):
        f = list(super(ModelForm, self).__iter__())
        get_field = lambda field_id: next((fld for fld in f if fld.id == field_id))
        return (get_field(field_id) for field_id in self.__order)

    # because some of the sqlalchemy types don't map so well to these types (some are relationships),
    # these are overrides.
    organisations = fields.SelectMultipleField(default=['1', '3'])
    profession = fields.SelectMultipleField()
    location = fields.SelectMultipleField()
    gender = fields.RadioField(___('Gender'), validators=[validators.required()], choices=[
        ('M', ___('Male')), ('F', ___('Female'))]
    )
    is_activist = fields.RadioField(___('Is activist'), validators=[validators.required()], choices=[
        ('1', ___('Yes')), ('0', ___('No'))]
    )