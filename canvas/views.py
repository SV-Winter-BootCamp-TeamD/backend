from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Canvas
from .serializers import CanvasSerializer

class CanvasCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CanvasSerializer(data=request.data)

        if serializer.is_valid():
            canvas=serializer.save()
            return Response({
                    "message": "캔버스 생성 성공하였습니다.",
                    "canvas_name":serializer.data["canvas_name"],
                    "canvas_id": canvas.id
                }, status = status.HTTP_201_CREATED)
        return Response({"message": "캔버스 생성 실패했습니다."}, status = status.HTTP_404_NOT_FOUND)

class CanvasUpdateDeleteView(APIView):

    def put(self, request, canvas_id, *args, **kwargs):
        canvas_name= request.data.get("canvas_name")

        try:
            canvas = Canvas.objects.get(id=canvas_id)
            canvas.canvas_name = canvas_name
            canvas.updated_at= timezone.now()
            canvas.save()
            return Response({"message": "캔버스 이름 수정 성공하였습니다."},status = status.HTTP_200_OK)
        except Canvas.DoesNotExist:
            return Response({"message": "캔버스 이름 수정 실패하였습니다."},status = status.HTTP_404_NOT_FOUND)

    def delete(self, request, canvas_id, *args, **kwargs):
        try:
            canvas = Canvas.objects.get(id=canvas_id)
            canvas.delete()
            canvas.deleted_at = timezone.now()
            return Response({"message": "캔버스 삭제 성공하였습니다."},status = status.HTTP_200_OK)
        except Canvas.DoesNotExist:
            return Response({"message": "캔버스 삭제 실패하였습니다."},status = status.HTTP_404_NOT_FOUND)
