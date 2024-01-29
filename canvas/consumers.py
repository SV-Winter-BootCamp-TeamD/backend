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

        user_id = text_data_json['user_id']
        component_id = text_data_json['component_id']

        if int(user_id) not in users:
            print("해당 유저가 없습니다.")
            await self.channel_layer.group_discard(self.canvas_group_id, self.channel_name)
            self.close();

        if text_data_json.get("type") == "position":
            position_x = text_data_json['position_x']
            position_y = text_data_json['position_y']

            await self.channel_layer.group_send(
                self.canvas_group_id,
                {
                    'type': 'position',
                    'user_id': user_id,
                    'component_id': component_id,
                    'position_x': position_x,
                    'position_y': position_y
                }
            )

        elif text_data_json.get("type") == "resize":
            width = text_data_json['width']
            height = text_data_json['height']
            rotate = text_data_json.get('rotate', 0)
            beforeTranslate_x = text_data_json['beforeTranslate_x']
            beforeTranslate_y = text_data_json['beforeTranslate_y']

            await self.channel_layer.group_send(
                self.canvas_group_id,
                {
                    'type': 'resize',
                    'user_id': user_id,
                    'component_id': component_id,
                    'width': width,
                    'height': height,
                    'rotate': rotate,
                    'beforeTranslate_x': beforeTranslate_x,
                    'beforeTranslate_y': beforeTranslate_y
                }
            )

        elif text_data_json.get("type") == "rotate":
            rotate = text_data_json['rotate']

            await self.channel_layer.group_send(
                self.canvas_group_id,
                {
                    'type': 'rotate',
                    'user_id': user_id,
                    'component_id': component_id,
                    'rotate': rotate
                }
            )

        elif text_data_json.get("type") == "add":
            component_url = text_data_json['component_url']
            component_type = text_data_json['component_type']

            await self.channel_layer.group_send(
                self.canvas_group_id,
                {
                    'type': 'add',
                    'user_id': user_id,
                    'component_id': component_id,
                    'component_url': component_url,
                    'component_type': component_type
                }
            )

        elif text_data_json.get("type") == "remove":

            await self.channel_layer.group_send(
                self.canvas_group_id,
                {
                    'type': 'remove',
                    'user_id': user_id,
                    'component_id': component_id
                }
            )

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
            'position_y': position_y
        }))

    async def resize(self, event):
        user_id = event['user_id']
        component_id = event['component_id']
        width = event['width']
        height = event['height']
        rotate = event['rotate']
        beforeTranslate_x = event['beforeTranslate_x']
        beforeTranslate_y = event['beforeTranslate_y']

        await self.send(text_data=json.dumps({
            'type': 'resize',
            'user_id': user_id,
            'component_id': component_id,
            'width': width,
            'height': height,
            'rotate': rotate,
            'beforeTranslate_x': beforeTranslate_x,
            'beforeTranslate_y': beforeTranslate_y
        }))

    async def rotate(self, event):
        user_id = event['user_id']
        component_id = event['component_id']
        rotate = event['rotate']

        await self.send(text_data=json.dumps({
            'type': 'rotate',
            'user_id': user_id,
            'component_id': component_id,
            'rotate': rotate
        }))

    async def add(self, event):
        user_id = event['user_id']
        component_id = event['component_id']
        component_url = event['component_url']
        component_type = event['component_type']

        await self.send(text_data=json.dumps({
            'type': 'add',
            'user_id': user_id,
            'component_id': component_id,
            'component_url': component_url,
            'component_type': component_type
        }))

    async def remove(self, event):
        user_id = event['user_id']
        component_id = event['component_id']

        await self.send(text_data=json.dumps({
            'type': 'remove',
            'user_id': user_id,
            'component_id': component_id
        }))