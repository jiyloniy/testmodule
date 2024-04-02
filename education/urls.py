from django.urls import path, include
from education.views import RoomViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')

urlpatterns = [
    path('', include(router.urls)),
]
