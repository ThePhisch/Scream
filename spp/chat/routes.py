from flask import render_template
from flask.helpers import url_for
from flask_login import current_user
from flask_login.utils import login_required
from werkzeug.utils import redirect
from spp.chat import bp
from spp.chat.forms import PostForm, RoomForm
from spp import db
from spp.models import Post, Room, User
from datetime import datetime


@bp.route('/chat/<room>', methods=["GET", "POST"])
@login_required
def chatroom(room):
    if list(Room.query.filter(Room.name == room)):
        form = PostForm()
        if form.validate_on_submit():
            post = Post(body=form.post.data,
                        author_id=current_user.id,
                        author_name=current_user.username,
                        room_name=room)

            db.session.add(post)
            db.session.commit()
            return redirect(f'/chat/{room}')
        posts = Post.query.filter(Post.room_name == room)
        return render_template("chat.html", form=form, posts=posts, room=room)
    else:
        return redirect(url_for('chat.chatnotfound'))


@bp.route('/lobby', methods=["GET", "POST"])
@login_required
def lobbyroom():
    form = RoomForm()
    if form.validate_on_submit():
        room = Room(name=form.room.data,
                    owner_id=current_user.id,
                    owner_name=current_user.username)
        db.session.add(room)
        db.session.commit()
        return redirect(url_for('chat.lobbyroom'))
    rooms = Room.query.all()
    return render_template("lobby.html", form=form, rooms=rooms)

@bp.route('/chatnotfound')
@login_required
def chatnotfound():
    return render_template("chatnotfound.html")