from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Score
from .serializers import ScoreSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class LeaderboardView(generics.ListAPIView):
    queryset = Score.objects.all().order_by('-score')
    serializer_class = ScoreSerializer

    def perform_create(self, serializer):
        user = self.request.user  # Используем пользователя из токена
        new_score = self.request.data.get('score')

        try:
            user_score = Score.objects.get(user=user)
            previous_score = user_score.score
        except Score.DoesNotExist:
            user_score = None
            previous_score = 0

        if user_score is None or new_score > previous_score:
            if user_score is None:
                user_score = Score(user=user, score=new_score)
            else:
                user_score.score = new_score
            user_score.save()

            serializer.save()
            return Response({'detail': 'Score updated successfully'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Score is not higher than the previous one'}, status=status.HTTP_400_BAD_REQUEST)

class UserScoreView(generics.UpdateAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        obj, created = Score.objects.get_or_create(user=user)
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.score = request.data.get('score', instance.score)
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

