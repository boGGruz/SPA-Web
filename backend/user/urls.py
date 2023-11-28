from django.urls import path
from .views import ScoreApi

urlpatterns = [
    path('', ScoreApi.as_view(), name='score-api'),
]