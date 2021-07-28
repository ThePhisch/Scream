from flask_wtf import FlaskForm
from wtforms.fields.simple import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    post = TextAreaField("Idea:",
                         validators=[DataRequired(), Length(min=1, max=140)
                                     ])
    submit = SubmitField("Scream!")
