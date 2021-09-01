from flask_socketio import SocketIO, emit, join_room
from model import app
from flask import render_template
import eventlet
from flask_login import current_user

socketio = SocketIO(app, async_mode='eventlet', logger=True)
eventlet.monkey_patch()


@app.route("/chat", methods=['POST', 'GET'])
def chat():
    return render_template("chat.html", current_user=current_user)


@socketio.on('client_create_room', namespace='/chat')
def handle_client_create_room(data):
    room = current_user.id
    print(current_user.name + ' is now ' + data['data'])
    emit('request_worker', {
        'data': f"{current_user.name} has joined the room [{room}]",
        'room': room
    })
    join_room(room)
    emit('sys_room_msg', {
        'data': f"You've joined the room [{room}]."
    }, to=room)


@socketio.on('client_text', namespace='/chat')
def text(data):
    emit('text_msg', {
        'data': data['data']
    })


def handle_worker_event():
    pass

