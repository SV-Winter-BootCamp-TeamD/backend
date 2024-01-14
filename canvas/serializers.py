from rest_framework import serializers
from .models import Canvas

class CanvasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Canvas
        fields = '__all__'

class CanvasPersonalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canvas
        fields = ['owner_id']
