from rest_framework import serializers
from component.serializers import ComponentSerializer
from user.models import User
from .models import Canvas

class CanvasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Canvas
        fields = '__all__'

class CanvasCreateSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canvas
        fields = ['canvas_name', 'owner_id']

class CanvasUpdateDeleteSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canvas
        fields = ['canvas_name']

class MemberInviteSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','user_email','user_name']

class ComponentSwaggerSerializer(serializers.Serializer):
    canvas_name = serializers.CharField()
    component_id = serializers.IntegerField()
    position_x = serializers.FloatField()
    position_y = serializers.FloatField()
    component_type = serializers.CharField()
    component_url = serializers.CharField()
    width = serializers.FloatField()
    height = serializers.FloatField()

class CanvasSaveSwaggerSerializer(serializers.Serializer):
    components = ComponentSerializer(many=True)
    canvas_preview_url = serializers.CharField()

class CanvasListSwaggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Canvas
        fields = ['id', 'canvas_name', 'canvas_preview_url', 'updated_at']