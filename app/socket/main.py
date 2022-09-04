import socketio

from app.models.chats import Chats, MessageModel, MessageUserModel

# create a Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins=[], async_mode='asgi')


###############################
# On Connect
###############################

@sio.event
async def connect(sid, environ, auth):
    print('connect ', sid)


###############################
# On Disconnect
###############################
@sio.event
async def disconnect(sid):
    print('disconnect ', sid)

###############################
# Subscribe to Room (UserId)
###############################


@sio.on('join-room')
async def join_room(sid, data):
    sio.enter_room(sid, data['room'])


###############################
# Send Message
###############################


@sio.on('message')
async def message(sid, data):

    # Application-wide Notification Socket
    await sio.emit('notification', {"content": data['content'], "user": data['user']}, room=data['room'])

    # Chat Message Socket
    await sio.emit('message', {"content": data['content'], "user": data['user']}, room=data['room'])

    # Save Chat Message to DB
    Chats.add_chat_message_by_user_ids([data['room'], data['user']['id']], MessageModel(**{
        "content": data['content'],
        "user": MessageUserModel(**{
            "id": data['user']['id'],
            "name": data['user']['name']
        })
    }))


# wrap with ASGI application
app = socketio.ASGIApp(sio)
