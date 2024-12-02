from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScoreViewSet, PlayerViewSet

router = DefaultRouter()
router.register(r'scores', ScoreViewSet)
router.register(r'players', PlayerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
