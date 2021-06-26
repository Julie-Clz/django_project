from django.contrib import admin
from .models import Hometeam, Match, Awayteam, Bet

admin.site.register(Hometeam)
admin.site.register(Match)
admin.site.register(Awayteam)
admin.site.register(Bet)