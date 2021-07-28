from flask import render_template
from flask.helpers import url_for
from flask_login import current_user
from flask_login.utils import login_required
from werkzeug.utils import redirect
from spp.chat import bp
from spp.chat.forms import PostForm
from spp import db
from spp.models import Post

@bp.route('/chat', methods=["GET", "POST"])
@login_required
def chatroom():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('chat.chatroom'))
    return render_template("chat.html", form=form)