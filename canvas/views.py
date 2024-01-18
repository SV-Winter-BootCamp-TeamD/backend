from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from component.models import Component
from user.models import User
from .models import Canvas, CanvasMember
from .serializers import CanvasSerializer, CanvasCreateSwaggerSerializer, CanvasUpdateDeleteSwaggerSerializer, MemberInviteSwaggerSerializer, CanvasSaveSwaggerSerializer, CanvasListSwaggerSerializer, ComponentSwaggerSerializer
from component.s3_utils import upload_file_to_s3
import json

class CanvasCreateView(APIView):
    @swagger_auto_schema(
        request_body=CanvasCreateSwaggerSerializer,
        operation_id="캔버스 생성",
        responses={200: "캔버스 생성 성공", 404: "캔버스 생성에 실패했습니다."}
    )
    def post(self, request, *args, **kwargs):
        serializer = CanvasSerializer(data=request.data)

        if serializer.is_valid():
            canvas=serializer.save()

            return Response({
                    "message": "캔버스 생성 성공하였습니다.",
                    "canvas_name":serializer.data["canvas_name"],
                    "canvas_id": canvas.id
                }, status = status.HTTP_200_OK)
        return Response({"message": "캔버스 생성 실패했습니다."}, status = status.HTTP_404_NOT_FOUND)

class CanvasUpdateDeleteView(APIView):
    @swagger_auto_schema(
        request_body=CanvasUpdateDeleteSwaggerSerializer,
        operation_id="캔버스 이름 변경/삭제",
        responses={200: "캔버스 삭제 성공", 404: "캔버스 삭제에 실패했습니다."}
    )
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

    @swagger_auto_schema(
        request_body=CanvasUpdateDeleteSwaggerSerializer,
        operation_id="캔버스 이름 변경/삭제",
        responses={200: "캔버스 이름 변경 성공", 404: "캔버스 이름 변경 실패했습니다."}
    )
    def delete(self, request, canvas_id, *args, **kwargs):
        try:
            canvas = Canvas.objects.get(id=canvas_id)
            canvas.delete()
            canvas.deleted_at = timezone.now()
            return Response({"message": "캔버스 삭제 성공하였습니다."},status = status.HTTP_200_OK)
        except Canvas.DoesNotExist:
            return Response({"message": "캔버스 삭제 실패하였습니다."},status = status.HTTP_404_NOT_FOUND)

class MemberInviteView(APIView):
    @swagger_auto_schema(
        request_body=MemberInviteSwaggerSerializer,
        operation_id="친구 초대",
        responses={200: MemberInviteSwaggerSerializer(many=False)}
    )
    def post(self, request, canvas_id):

        user_email = request.data.get('user_email')

        try:
            user = User.objects.get(user_email=user_email)
        except User.DoesNotExist:
            return Response({'message': '해당 유저가 존재하지 않습니다.',
                            'result': None}, status=status.HTTP_404_NOT_FOUND)

        try:
            canvas = Canvas.objects.get(pk=canvas_id)
        except Canvas.DoesNotExist:
            return Response({'message': '해당 캔버스가 존재하지 않습니다.',
                            'result': None}, status=status.HTTP_404_NOT_FOUND)

        try:
            CanvasMember.objects.get(canvas_id=canvas_id, member_id=user.id)
        except CanvasMember.DoesNotExist:
            canvasmember = CanvasMember(
                canvas_id=canvas,
                member_id=user.id,
                created_at=timezone.now(),
                updated_at=timezone.now(),
                deleted_at=None
            )
            canvasmember.save()

            return Response({'message': "친구 초대 성공",
                                 'result': {
                                     'user_email': user.user_name}}, status=status.HTTP_200_OK)
        return Response({'message': '친구 초대에 실패했습니다.',
                                 'result': None}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_id="친구 초대",
        responses={200: MemberInviteSwaggerSerializer(many=False)}
    )
    def get(self, request, canvas_id):
        try:
            canvas = Canvas.objects.get(id=canvas_id)
            share_member_list = []

            if CanvasMember.objects.filter(canvas_id=canvas_id).exists():
                members = CanvasMember.objects.filter(canvas_id=canvas_id).values('member_id', 'created_at', 'updated_at')
                for member in members:
                    user = User.objects.get(id=member['member_id'])
                    share_member_list.append({
                        'user_id': member['member_id'],
                        'user_email': user.user_email,
                        'user_name': user.user_name
                    })

            response_data = {
                'shared_members': share_member_list,
            }

            return Response({
                'message': '초대 목록 조회 성공',
                'result': response_data
            }, status=status.HTTP_200_OK)
        except Canvas.DoesNotExist:
            return Response({
                'message': '존재하지 않는 캔버스 ID입니다.',
                'result': None
            }, status=status.HTTP_404_NOT_FOUND)

class CanvasSaveView(APIView):
    @swagger_auto_schema(
        request_body=CanvasSaveSwaggerSerializer,
        operation_id="캔버스 저장",
        responses={200: CanvasSaveSwaggerSerializer(many=False)}
    )
    def put(self, request, canvas_id):

        components = json.loads(request.data.get('components', []))

        for component_data in components:
            component_id = component_data.get('component_id')
            position_x = component_data.get('position_x')
            position_y = component_data.get('position_y')
            width = component_data.get('width')
            height = component_data.get('height')
            component_url = component_data.get('component_url')

            try:
                component = Component.objects.get(pk=component_id)
                if component.canvas_id.pk != canvas_id:
                    return Response({"message": "존재하지 않는 캔버스 ID입니다."}, status=status.HTTP_404_NOT_FOUND)

                component.position_x = position_x
                component.position_y = position_y
                component.width = width
                component.height = height
                component.component_url = component_url
                component.save()

            except Component.DoesNotExist:
                return Response({
                    'message': '해당 요소를 찾을 수 없습니다.',
                    'result': None
                }, status=status.HTTP_404_NOT_FOUND)

        try:
            canvas = Canvas.objects.get(pk=canvas_id)
            canvas_preview_url = request.FILES.get('canvas_preview_url')

            if not canvas_preview_url:
                return Response({"message": "업로드할 파일이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

            key = f"preview/{canvas_id}"
            ExtraArgs = {'ContentType': canvas_preview_url.content_type}
            file_url = upload_file_to_s3(canvas_preview_url, key, ExtraArgs)

            if not file_url:
                return Response({"message": "S3 버킷에 파일 업로드 실패"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            canvas.canvas_preview_url = file_url
            canvas.save()

            return Response({"message": "캔버스 저장 성공"}, status=status.HTTP_200_OK)

        except Canvas.DoesNotExist:
            return Response({
                "message": "존재하지 않는 캔버스 ID입니다.",
                "result": None
            }, status=status.HTTP_404_NOT_FOUND)

class CanvasPersonalListView(APIView):
    @swagger_auto_schema(
        operation_id="개인 캔버스 전체 조회",
        responses={200: CanvasListSwaggerSerializer(many=False)}
    )
    def get(self, request, user_id):
        canvases = Canvas.objects.filter(owner_id=user_id)

        canvas_list = []
        for canvas in canvases:
            canvas_data = {
                "canvas_id": canvas.id,
                "canvas_preview_url": canvas.canvas_preview_url,
                "canvas_name": canvas.canvas_name,
                "update_at": canvas.updated_at,
            }
            canvas_list.append(canvas_data)

        return Response({
            "message": "개인 캔버스 전체 조회 성공",
            "result": {
                "canvases": canvas_list
            }
        }, status=status.HTTP_200_OK)

class CanvasShareListView(APIView):
    @swagger_auto_schema(
        operation_id="공유 캔버스 전체 조회",
        responses={200: CanvasListSwaggerSerializer(many=False)}
    )
    def get(self, request, user_id):
        canvases = CanvasMember.objects.filter(member_id=user_id).values_list('canvas_id', flat=True)
        shared_canvases = Canvas.objects.filter(id__in=canvases)

        canvas_list = []
        for canvas in shared_canvases:
            canvas_data = {
                "canvas_id": canvas.id,
                "canvas_preview_url": canvas.canvas_preview_url,
                "canvas_name": canvas.canvas_name,
                "update_at": canvas.updated_at,
            }
            canvas_list.append(canvas_data)

        return Response({
            "message": "공유 캔버스 전체 조회 성공",
            "result": {
                "canvases": canvas_list
            }
        }, status=status.HTTP_200_OK)


class CanvasDetailSearchView(APIView):
    @swagger_auto_schema(
        operation_id="캔버스 상세 조회",
        responses={200: ComponentSwaggerSerializer(many=False)}
    )
    def get(self, request, canvas_id):
        try:
            canvas = Canvas.objects.get(id=canvas_id)
            latest_background = Component.objects.filter(canvas_id=canvas_id, component_type='Background').order_by('-updated_at').first()
            stickers = Component.objects.filter(canvas_id=canvas_id).exclude(component_type='Background').values('id', 'component_type', 'component_url', 'position_x', 'position_y', 'width', 'height')

            response_data = {
                'canvas_name': canvas.canvas_name,
                'background': {
                    'id': latest_background.id,
                    'component_type': latest_background.component_type,
                    'component_url': latest_background.component_url,
                    'position_x': latest_background.position_x,
                    'position_y': latest_background.position_y,
                    'width': latest_background.width,
                    'height': latest_background.height,
                },
                'sticker': stickers,
            }

            return Response({
                'message': '캔버스 상세 조회 성공했습니다.',
                'result': response_data
            }, status=status.HTTP_200_OK)

        except Canvas.DoesNotExist:
            return Response({
                'message': '존재하지 않는 캔버스 ID입니다.',
                'result': None
            }, status=status.HTTP_404_NOT_FOUND)
