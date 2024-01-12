from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Component
from canvas.models import Canvas
from .s3_utils import upload_file_to_s3

class BackgroundUploadView(APIView):
    def post(self, request, canvas_id, *args, **kwargs):
        try:
            canvas = Canvas.objects.get(id=canvas_id)
            file = request.FILES.get('file')
            if not file:
                return Response({"message": "업로드할 파일이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

            component_type = request.data.get('component_type', 'Background')
            component_source = request.data.get('component_source', 'Upload')

            key = f"{canvas_id}/background/{file.name}"
            ExtraArgs = {'ContentType': file.content_type}

            file_url = upload_file_to_s3(file, key, ExtraArgs)
            if not file_url:
                return Response({"message": "S3 버킷에 파일 업로드 실패"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            component = Component.objects.create(
                canvas_id=canvas,
                component_type=component_type,
                component_source=component_source,
                component_url=file_url,
                position_x=0.0,
                position_y=0.0
            )

            return Response({
                "message": "직접 배경 업로드 성공",
                "result": {
                    "component": {
                        "component_id": component.id,
                        "component_type": component_type,
                        "component_source": component_source
                    }
                }
            }, status=status.HTTP_201_CREATED)
        except Canvas.DoesNotExist:
            return Response({
                "message": "존재하지 않는 캔버스 ID입니다.",
                "result": None
            }, status=status.HTTP_404_NOT_FOUND)
