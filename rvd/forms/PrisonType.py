from wtforms_alchemy import ModelForm
from rvd.models import PrisonType


class PrisonTypeForm(ModelForm):

    class Meta:
        model = PrisonType