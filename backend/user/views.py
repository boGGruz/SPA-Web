from .models import Score
from .serializers import ScoreSerializer
from rest_framework.views import APIView

class ScoreApi(APIView):
    queryset = Score.objects.all()
    serializer_for_queryset = ScoreSerializer
