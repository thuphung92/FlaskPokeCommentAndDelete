from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    class Meta:
        csrf = False # disable CSRF protection
    pokemon_name = StringField('Pokemon name', validators=[DataRequired()])
    submit = SubmitField('Submit')