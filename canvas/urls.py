from django.urls import path
from .views import CanvasCreateView, CanvasUpdateDeleteView, MemberInvite
from component.views import BackgroundUploadView, BackgroundAIView, StickerAIView, TextUploadView

urlpatterns = [
    path('', CanvasCreateView.as_view(), name='create-canvas'),
    path('<int:canvas_id>/', CanvasUpdateDeleteView.as_view(), name='update/delete-canvas'),
    path('<int:canvas_id>/invite/', MemberInvite.as_view(), name='invite-canvas'),
    path('<int:canvas_id>/backgrounds/upload/', BackgroundUploadView.as_view(), name='background-upload'),
    path('<int:canvas_id>/texts/upload/', TextUploadView.as_view(), name='text-upload'),
    path('<int:canvas_id>/backgrounds/ai/', BackgroundAIView.as_view(), name='background-ai'),
    path('<int:canvas_id>/stickers/ai/', StickerAIView.as_view(), name='sticker-ai'),
]