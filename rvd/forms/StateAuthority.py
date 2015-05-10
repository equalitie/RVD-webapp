from wtforms_alchemy import ModelForm
from rvd.models import StateAuthority


class StateAuthorityForm(ModelForm):

    class Meta:
        model = StateAuthority
