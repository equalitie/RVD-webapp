from wtforms_alchemy import ModelForm
from rvd.models import InternationalAuthority


class InternationalAuthorityForm(ModelForm):

    class Meta:
        model = InternationalAuthority
