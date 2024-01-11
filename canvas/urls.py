from django.urls import path
from .views import CanvasCreateView, CanvasUpdateView

urlpatterns = [
    path('', CanvasCreateView.as_view(), name='create-canvas'),
    path('<int:canvas_id>/', CanvasUpdateView.as_view(), name='update/delete-canvas'),
]