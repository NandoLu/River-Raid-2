from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Score, Player
from .serializers import ScoreSerializer, PlayerSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer

    def create(self, request, *args, **kwargs):
        player_id = request.data.get('player')
        score_value = request.data.get('score')

        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return Response({"error": "Player not found"}, status=status.HTTP_404_NOT_FOUND)

        # Verifica se já existe um score para este jogador
        existing_score = Score.objects.filter(player=player).order_by('-score').first()

        if existing_score and existing_score.score >= int(score_value):
            return Response({"message": "Existing score is higher or equal. No update needed."}, status=status.HTTP_200_OK)

        # Se não existir ou a nova pontuação for maior, salva a nova pontuação
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
