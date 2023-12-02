from django.urls import path
from .views import LeaderboardView, UserScoreView

urlpatterns = [
    path('', UserScoreView.as_view(), name='user-score'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]
