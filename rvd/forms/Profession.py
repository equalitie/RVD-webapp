from wtforms_alchemy import ModelForm
from rvd.models import Profession


class ProfessionForm(ModelForm):

    class Meta:
        model = Profession
