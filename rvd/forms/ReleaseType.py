from wtforms_alchemy import ModelForm
from rvd.models import ReleaseType


class ReleaseTypeForm(ModelForm):

    class Meta:
        model = ReleaseType

