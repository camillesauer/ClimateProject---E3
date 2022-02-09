# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired

class ImgForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    file = FileField()
    submit = SubmitField('Submit')
