from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    post = TextAreaField("Idea:",
                         validators=[DataRequired(), Length(min=1, max=300)
                                     ])
    submit = SubmitField("Scream!")


class RoomForm(FlaskForm):
    room = TextAreaField("New Room:",
                         validators=[DataRequired(), Length(min=1, max=60)])
    submit = SubmitField("Create")