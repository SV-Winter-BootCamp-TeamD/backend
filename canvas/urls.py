from django.urls import path
from .views import CanvasCreateView

urlpatterns = [
    path('', CanvasCreateView.as_view(), name='create-canvas'),
]