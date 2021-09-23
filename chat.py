from flask_socketio import SocketIO, emit, join_room
from model import app
from flask import render_template
import eventlet
from flask_login import current_user
from flask import request

socketio = SocketIO(app, async_mode='eventlet', logger=True)
eventlet.monkey_patch()
secret_code = '000000000'


@app.route("/chat", methods=['POST', 'GET'])
def chat():
    return render_template("chat.html", current_user=current_user)


@socketio.on('client_create_room', namespace='/chat')
def handle_client_create_room(data):
    location = request.sid
    name = current_user.name
    print(name + ' is now ' + data['data'])
    emit('sys_room_msg', {
        'data': f"You've joined the room [{location}]."
    }, to=location)


@socketio.on('client_text', namespace='/chat')
def text(data):
    location = request.sid
    name = current_user.name
    msg_data = data['data']
    if msg_data == secret_code:
        join_room(secret_code)
        print(name + ' is now ' + f'in room {secret_code}')
        emit('sys_to_room_0_msg', {
            'data': f'Joined Room {secret_code}!'}, to=secret_code)
    else:
        emit('text_msg', {
            'name': name,
            'data': msg_data},
             to=location)
        emit('to_room_0_msg', {
            'room': location,
            'name': name,
            'data': msg_data
        }, to=secret_code)


@socketio.on('room_0_to_room_msg', namespace='/chat')
def deliver_text_to_room(data):
    room = data['room']
    text_data = data['data']
    emit('text_msg', {
        'name': 'Worker',
        'data': text_data
    }, to=room)
    emit('to_room_0_msg', {
        'room': room,
        'name': 'You',
        'data': text_data
    }, to=secret_code)


