from django.urls import path
from .views import MatchListView
from . import views

urlpatterns = [
    path('', MatchListView.as_view(), name='pronos-match-index'),
]
