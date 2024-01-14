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
        user_id = text_data_json['user_id']
        component_id = text_data_json['component_id']
        position_x = text_data_json['position_x']
        position_y = text_data_json['position_y']

        print(text_data_json)
        canvas_id = self.scope["url_route"]["kwargs"]["canvas_id"]

        ## 유저 인증 로직
        canvas = Canvas.objects.get(id=canvas_id)
        users = [canvas.owner_id]
        canvasmembers = CanvasMember.objects.filter(canvas_id=canvas_id)

        for canvasmember in canvasmembers:
            users.append(canvasmember.member_id)

        if user_id in users:
            print("유저 확인 완료")
            await self.channel_layer.group_send(
                self.canvas_group_id,
                {
                    'type': 'canvas.message',
                    'user_id': user_id,
                    'component_id': component_id,
                    'position_x': position_x,
                    'position_y': position_y,
                }
            )
        else:
            print("해당 유저가 없습니다.")
            # await self.channel_layer.group_discard(self.canvas_group_id, self.channel_name)
            # self.close();

    async def canvas_message(self, event):
        user_id = event['user_id']
        component_id = event['component_id']
        position_x = event['position_x']
        position_y = event['position_y']

        await self.send(text_data=json.dumps({
            'user_id': user_id,
            'component_id': component_id,
            'position_x': position_x,
            'position_y': position_y,
        }))
