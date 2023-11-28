from rest_framework import serializers
from .models import Score
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ScoreSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Score
        fields = ['user', 'score']

