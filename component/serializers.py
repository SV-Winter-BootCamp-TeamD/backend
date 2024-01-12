from rest_framework import serializers
from .models import Component

class BackgroundUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ['id', 'component_url']

class TextUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ['component_url']
