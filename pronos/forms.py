from django import forms
from .models import Bet, Userteam, UserteamMember


class BetCreateForm(forms.ModelForm):
    match = forms.Select()
    hometeam = forms.Select()
    awayteam = forms.Select()
    user = forms.Select()
    prono_hometeam = forms.IntegerField()
    prono_awayteam = forms.IntegerField()
    tab = forms.CheckboxInput()
    TEAMS = (
        (''),
        (hometeam),
        (awayteam),
    )
    winner = forms.Select(choices=TEAMS)

    class Meta:
        model = Bet
        fields = ['user', 'match', 'hometeam','awayteam', 'prono_hometeam', 'prono_awayteam', 'tab', 'winner']


class UserteamcreateForm(forms.ModelForm):
    class Meta:
        model = Userteam
        fields = ['name']

class UserteamJoinform(forms.ModelForm):
    userteam = forms.ModelChoiceField(queryset=Userteam.objects.all())

    class Meta:
        model = UserteamMember
        fields = ['userteam']
        
