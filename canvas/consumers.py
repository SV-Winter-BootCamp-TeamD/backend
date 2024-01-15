import json

from channels.generic.websocket import AsyncWebsocketConsumer
from canvas.models import CanvasMember, Canvas


class CanvasConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.canvas_id = self.scope["url_route"]["kwargs"]["canvas_id"]
        self.canvas_group_id = "canvas_group_%s" % self.canvas_id

        await self.channel_layer.group_add(self.canvas_group_id, self.channel_name)  # 그룹으로 참여
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.canvas_group_id, self.channel_name)

    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
        canvas_id = self.scope["url_route"]["kwargs"]["canvas_id"]

        ## 유저 인증 로직
        canvas = Canvas.objects.get(id=canvas_id)
        users = [canvas.owner_id]
        canvasmembers = CanvasMember.objects.filter(canvas_id=canvas_id)

        for canvasmember in canvasmembers:
            users.append(canvasmember.member_id)

        if text_data_json.get("type") == "position":

            user_id = text_data_json['user_id']
            component_id = text_data_json['component_id']
            position_x = text_data_json['position_x']
            position_y = text_data_json['position_y']

            if user_id in users:
                print("유저 확인 완료")
                await self.channel_layer.group_send(
                    self.canvas_group_id,
                    {
                        'type': 'position',
                        'user_id': user_id,
                        'component_id': component_id,
                        'position_x': position_x,
                        'position_y': position_y,
                    }
                )
            else:
                print("해당 유저가 없습니다.")
                await self.channel_layer.group_discard(self.canvas_group_id, self.channel_name)
                self.close();

        elif text_data_json.get("type") == "resize":

            user_id = text_data_json['user_id']
            component_id = text_data_json['component_id']
            width = text_data_json['width']
            height = text_data_json['height']

            if user_id in users:
                print("유저 확인 완료")
                await self.channel_layer.group_send(
                    self.canvas_group_id,
                    {
                        'type': 'resize',
                        'user_id': user_id,
                        'component_id': component_id,
                        'width': width,
                        'height': height,
                    }
                )
            else:
                print("해당 유저가 없습니다.")
                await self.channel_layer.group_discard(self.canvas_group_id, self.channel_name)
                self.close();

    async def position(self, event):
        user_id = event['user_id']
        component_id = event['component_id']
        position_x = event['position_x']
        position_y = event['position_y']

        await self.send(text_data=json.dumps({
            'type': 'position',
            'user_id': user_id,
            'component_id': component_id,
            'position_x': position_x,
            'position_y': position_y,
        }))

    async def resize(self, event):
        user_id = event['user_id']
        component_id = event['component_id']
        width = event['width']
        height = event['height']

        await self.send(text_data=json.dumps({
            'type': 'resize',
            'user_id': user_id,
            'component_id': component_id,
            'width': width,
            'height': height,
        }))