# app/admin/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired
from ..models import Role, Img
from wtforms_sqlalchemy.fields import QuerySelectField


class ImgForm(FlaskForm):
    """
    Form for admin to add or edit an image
    """
    name = StringField('Name', validators=[DataRequired()])
    file = FileField()
    submit = SubmitField('Submit')


class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to employees
    """
    img = QuerySelectField(query_factory=lambda: Img.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')
