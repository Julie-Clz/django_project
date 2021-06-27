from django.urls import path
from .views import MatchListView, BetListView, BetCreateView, BetDetailView, BetUpdateView, BetDeleteView
from . import views

urlpatterns = [
    path('', MatchListView.as_view(), name='match-index'),
    path('index/', BetListView.as_view(), name='bet-index'),
    path('bet/new/', views.BetCreateView, name='bet-create'),
    path('bet/<int:pk>/', BetDetailView.as_view(), name='bet-detail'),
    path('bet/<int:pk>/update/', BetUpdateView.as_view(), name='bet-update'),
    path('bet/<int:pk>/delete/', BetDeleteView.as_view(), name='bet-delete'),
]
