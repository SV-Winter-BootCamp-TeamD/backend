from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CanvasSerializer
from rest_framework import status

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