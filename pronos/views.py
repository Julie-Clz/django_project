from pronos.models import Hometeam, Match
from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse


# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")


class MatchListView(ListView):
    model = Match
    template_name = 'pronos/match_index.html' # <app>/<model>_<viewtype>.html
    context_object_name = 'matchs'
    # paginate_by = 5

