from django.urls import path
from .views import CanvasCreateView, CanvasUpdateDeleteView, MemberInvite

urlpatterns = [
    path('', CanvasCreateView.as_view(), name='create-canvas'),
    path('<int:canvas_id>/', CanvasUpdateDeleteView.as_view(), name='update/delete-canvas'),
    path('<int:canvas_id>/invite/', MemberInvite.as_view(), name='invite-canvas'),
]