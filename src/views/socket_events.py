from flask_login import current_user
from flask_socketio import join_room, emit
from __main__ import db, socketio
from models.models import ChatMessage


@socketio.on("join_task_chat")
def handle_join_task_chat(data):
    task_id = data["task_id"]
    room = f"task_{task_id}"
    join_room(room)
    emit("joined_task_chat", {"message": "Joined task chat"}, room=room)


@socketio.on("send_task_message")
def handle_send_task_message(data):
    task_id = data["task_id"]
    new_message = ChatMessage(task_id=task_id, sender_id=current_user.id, text=data["text"])
    db.session.add(new_message)
    db.session.commit()
    room = f"task_{task_id}"
    emit("new_task_message", new_message.serialize(), room=room)
