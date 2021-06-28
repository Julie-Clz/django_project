from django import forms
from .models import Bet, Userteam

class BetCreateForm(forms.ModelForm):
    match = forms.Select()
    hometeam = forms.Select()
    awayteam = forms.Select()
    user = forms.Select()
    prono_hometeam = forms.IntegerField()
    prono_awayteam = forms.IntegerField()

    class Meta:
        model = Bet
        fields = ['user', 'match', 'hometeam','awayteam', 'prono_hometeam', 'prono_awayteam']


class UserteamcreateForm(forms.ModelForm):
    class Meta:
        model = Userteam
        fields = ['name', 'image']
