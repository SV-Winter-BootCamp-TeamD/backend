from rest_framework import serializers
from .models import Canvas

class CanvasCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Canvas
        fields = ['canvas_name', 'owner_id']

class CanvasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Canvas
        fields = '__all__'