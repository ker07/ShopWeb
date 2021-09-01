from flask_socketio import emit, join_room
from model import app
from flask import render_template
from chat import socketio
from flask_login import current_user


@app.route("/workerchat", methods=['GET', 'POST'])
def workerchat():
    return render_template('workerchat.html', current_user=current_user)
