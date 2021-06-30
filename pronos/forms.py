from django import forms
from .models import Awayteam, Bet, Hometeam, Match, Userteam, UserteamMember

class BetCreateForm(forms.ModelForm):
    match = forms.ModelChoiceField(queryset=Match.objects.all())
    hometeam = forms.ModelChoiceField(queryset=Hometeam.objects.all())
    awayteam = forms.ModelChoiceField(queryset=Awayteam.objects.all())
    user = forms.Select()
    prono_hometeam = forms.IntegerField()
    prono_awayteam = forms.IntegerField()

    class Meta:
        model = Bet
        fields = ['user', 'match', 'hometeam','awayteam', 'prono_hometeam', 'prono_awayteam']


class UserteamcreateForm(forms.ModelForm):
    class Meta:
        model = Userteam
        fields = ['name']


class UserteamJoinform(forms.ModelForm):
    userteam = forms.ModelChoiceField(queryset=Userteam.objects.all())

    class Meta:
        model = UserteamMember
        fields = ['userteam']
        
