from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class AnimeForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    sypnosis = StringField('Sypnosis', validators=[DataRequired()],  widget=TextArea())
    genres = StringField('Genre', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ParseAnimeForm(FlaskForm):
    url = StringField('Url', validators=[DataRequired()])
    parse = SubmitField('Parse')
