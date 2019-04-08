import asyncio
import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from uuid import uuid4
from delivery.models import Task, TaskActivity
# from delivery.handlers.mgr_task import ManagerTask
from delivery.dbapi import TaskDbio
from delivery.handlers.dvr_task import DeliveryPerson
# from chat.handlers.logic import TicketAct


class TaskConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        await self.send({
            'type': 'websocket.accept'
        })
        print(self.scope['user'])
        # import ipdb; ipdb.set_trace()
        # here take the obj which have to be update
        # thread_obj = await self.get_test_obj()
        t = uuid4().hex
        # print(t_obj)
        # self.thread_obj = thread_obj
        # await asyncio.sleep(10)
        chat_room = f"thread_{t}"
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )
        # await asyncio.sleep(10)
        await self.send({
            'type': 'websocket.send'
        })

    async def websocket_receive(self, event):
        print('receive', event)
        # import ipdb; ipdb.set_trace()
        front_text = event.get('text', None)
        if front_text is not None:
            # receiving data from frontend
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data
            print(msg)
            user = self.scope['user']
            username = 'default'
            if user.is_authenticated:
                username = user.username
            myResponse = {
                'data': msg,
                'username': username
            }
            await self.create_new_task(user, msg)
            # reverse('get_cur_task')
            # await CurTaskConsumer(AsyncConsumer).websocket_connect(event)
            # sending data to frontend
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    'type': 'chat_message',
                    'text': json.dumps(myResponse)
                }
            )
        # {'type': 'websocket.receive', 'text': '{"message":"another"}'}

    async def chat_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    # async def websocket_disconnect(self, event):
    #     print('disconnected', event)

    # @database_sync_to_async
    # def get_test_obj(self):
    #     return Task.objects.all().last()

    @database_sync_to_async
    def create_new_task(self, me, data):
        task_data = {
            'title': data.get('title'),
            'content': data.get('content'),
            'priority': data.get('priority'),
            'created_by': me.profile
        }
        return TaskDbio().create_obj(task_data)


class CurTaskConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        await self.send({
            'type': 'websocket.accept'
        })
        print(self.scope['user'])

        t = uuid4().hex

        chat_room = f"thread_{t}"
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            chat_room,
            self.channel_name
        )

        m1 = await self.new_task()

        myResponse = {
            'title': m1.title,
            'content': m1.content,
            'priority': m1.priority,
            'state': m1.state,
            'created_by': m1.created_by.user.username
        }

        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat_message',
                'text': json.dumps(myResponse)
            }
        )

    async def chat_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def websocket_receive(self, event):
        print('receive', event)

    async def new_task(self):
        return DeliveryPerson().get_by_priority()
