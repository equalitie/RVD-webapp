from flask_babel import lazy_gettext as ___
from wtforms import Form, StringField

class DocumentUploadForm(Form):
    organisation_name = StringField(___('Organisation Name'))
