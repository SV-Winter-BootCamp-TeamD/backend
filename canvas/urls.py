
from django.urls import path, re_path
from .consumers import CanvasConsumer
from .views import CanvasCreateView, CanvasUpdateDeleteView, MemberInviteView, CanvasSaveView, CanvasPersonalListView, CanvasShareListView, CanvasDetailSearchView
from component.views import BackgroundUploadView, BackgroundAIView, BackgroundSelectView, StickerAIView, StickerSelectView, TextUploadView, ComponentDeleteView, BackgroundRecommendView

urlpatterns = [
    path('', CanvasCreateView.as_view(), name='create-canvas'),
    path('<int:canvas_id>/', CanvasUpdateDeleteView.as_view(), name='update/delete-canvas'),
    re_path(r'ws/canvases/(?P<canvas_id>\w+)/$', CanvasConsumer.as_asgi(), name='canvas-edit'),
    path('<int:canvas_id>/invite/', MemberInviteView.as_view(), name='invite-canvas'),
    path('<int:canvas_id>/backgrounds/upload/', BackgroundUploadView.as_view(), name='background-upload'),
    path('<int:canvas_id>/texts/upload/', TextUploadView.as_view(), name='text-upload'),
    path('<int:canvas_id>/backgrounds/ai/', BackgroundAIView.as_view(), name='background-ai'),
    path('<int:canvas_id>/backgrounds/ai/select/', BackgroundSelectView.as_view(), name='background-ai-select'),
    path('<int:canvas_id>/stickers/ai/', StickerAIView.as_view(), name='sticker-ai'),
    path('<int:canvas_id>/stickers/ai/select/', StickerSelectView.as_view(), name='sticker-ai-select'),
    path('<int:canvas_id>/<int:component_id>/', ComponentDeleteView.as_view(), name='component-delete'),
    path('<int:canvas_id>/save/', CanvasSaveView.as_view(), name='canvas-save'),
    path('<int:canvas_id>/backgrounds/recommend/', BackgroundRecommendView.as_view(), name='background-recommend'),
    path('personal/<int:user_id>/', CanvasPersonalListView.as_view(), name='canvas-list'),
    path('share/<int:user_id>/', CanvasShareListView.as_view(), name='canvas-share-lists'),
    path('detail/<int:canvas_id>/', CanvasDetailSearchView.as_view(), name='canvas-detail-search')
]