from django.urls import path
from .views import MatchListView, BetListView, BetCreateView
from . import views

urlpatterns = [
    path('', MatchListView.as_view(), name='pronos-match-index'),
    path('index/', BetListView.as_view(), name='pronos-bet-index'),
    path('bet/new/', views.BetCreateView, name='pronos-bet-create'),
]
