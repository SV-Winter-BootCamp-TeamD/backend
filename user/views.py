from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserLoginSwaggerSerializer
from django.contrib.auth import authenticate

class UserRegisterView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        operation_id="회원가입",
        responses={200: UserSerializer(many=False)}
    )
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입에 성공했습니다."}, status=status.HTTP_201_CREATED)
        return Response({"message": "회원가입에 실패했습니다."}, status=status.HTTP_404_NOT_FOUND)

class UserLoginView(APIView):
    @swagger_auto_schema(
        request_body=UserLoginSwaggerSerializer,
        operation_id="로그인",
        responses={200: UserLoginSwaggerSerializer(many=False)}
    )
    def post(self, request, *args, **kwargs):
        user_email = request.data.get('user_email')
        user_password = request.data.get('user_password')
        user = authenticate(username=user_email, password=user_password)

        if user is not None:
            return Response({
                "message": "로그인에 성공했습니다.",
                "result": {
                    "user_id": user.id,
                    "user_name": user.user_name
                }
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "로그인에 실패했습니다.",
            "result": None
        }, status=status.HTTP_404_NOT_FOUND)
