from django.urls import path
from .views import CanvasCreateView, CanvasUpdateDeleteView

urlpatterns = [
    path('', CanvasCreateView.as_view(), name='create-canvas'),
    path('<int:canvas_id>/', CanvasUpdateDeleteView.as_view(), name='update/delete-canvas'),
]