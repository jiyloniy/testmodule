from rest_framework import serializers
from education.models import Lesson, Room, Course, Order, Attendance


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('name',)
