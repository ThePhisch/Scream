from spp import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
from flask import current_app


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(300))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author_name = db.Column(db.String(60))
    room_name = db.Column(db.String(60), db.ForeignKey("room.name"))

    def __repr__(self) -> str:
        return f'<Post {self.id} by {self.author_name} in {self.room_name}>'

    def __str__(self) -> str:
        return f'<Post {self.body}>'

    def get_time(self) -> str:
        return self.timestamp.strftime(current_app.config['TIMEFORMAT'])

    def delete(self) -> None:
        Post.query.filter_by(id=self.id).delete()
        db.session.commit()



class Room(db.Model):
    name = db.Column(db.String(60), primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    owner_name = db.Column(db.String(60))

    def __repr__(self):
        return f'<Room {self.name} by {self.owner_id}>'

    def __str__(self):
        return f'<Room {self.name} by {self.owner_name}>'

    def get_time(self) -> str:
        return self.timestamp.strftime(current_app.config['TIMEFORMAT'])

    def closeroom(self) -> None:
        allposts = self.get_all_posts()
        print(allposts)
        for post in allposts:
            post.delete()
        Room.query.filter_by(name=self.name).delete()
        db.session.commit()


    def get_all_posts(self) -> list:
        return Post.query.filter_by(room_name=self.name).all()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
