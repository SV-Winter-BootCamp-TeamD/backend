from rest_framework import serializers
from .models import Component

class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ['id', 'component_url']
        ref_name = 'Components'

class TextUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ['component_url']

class TextResponseSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ['id', 'component_type', 'component_source', 'component_url']

class BackgroundSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ['id', 'component_type', 'component_source']

class SelectSwaggerSerializer(serializers.Serializer):
    selected_url = serializers.URLField(required=True)

class BackgroundUploadSwaggerSerializer(serializers.Serializer):
    file = serializers.URLField(required=True)

class BackgroundAISwaggerSerializer(serializers.Serializer):
    color = serializers.CharField(required=True)
    theme = serializers.CharField(required=True)
    place = serializers.CharField(required=True)

class StickerAISwaggerSerializer(serializers.Serializer):
    describe = serializers.CharField(required=True)
    style = serializers.CharField(required=True)

class AIResponseSwaggerSerializer(serializers.Serializer):
    canvas_id = serializers.IntegerField()
    s3_urls = serializers.ListField(child=serializers.URLField())

class BackgroundRecommendSwaggerSerializer(serializers.Serializer):
    image_url = serializers.URLField(required=True)
