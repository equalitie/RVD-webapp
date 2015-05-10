from wtforms_alchemy import ModelForm
from rvd.models import RightsViolation


class RightsViolationForm(ModelForm):

    class Meta:
        model = RightsViolation