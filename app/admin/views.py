# app/admin/views.py
from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from . import admin, user
from flask import Flask
from . forms import ImgForm, UserAssignForm, RoleForm
from .. import db
from ..models import Img, Role, User
import sys
import os
import os.path
sys.path.append(os.path.abspath("/home/apprenant/PycharmProjects/ClimateProject---E3/model"))
from model.load import predict



def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

@admin.route('/images/', methods=['GET'])
@login_required
def list_images():
    """
    List all images
    """
    images = Img.query.filter_by(user_id=current_user.id).all()
    return render_template('admin/images/images.html',
                           images=images,title="images")


@admin.route('/images/add', methods=['GET', 'POST'])
@login_required
def add_img():
    """
    Add an image to the database
    """
    add_img = True

    form = ImgForm()
    if form.validate_on_submit():
        app = Flask(__name__, instance_relative_config=True)
        filename = secure_filename(form.file.data.filename)
        UPLOAD_FOLDER = '/app/static/uploads'
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        form.file.data.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        prediction = predict(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        img = Img(name=filename, user_id=current_user.id, img=filename, mimetype=form.file.data.mimetype, prediction=prediction[0], out=prediction[1])
        db.session.add(img)
        db.session.commit()
        flash("Congratulations, your item has been added")
        # redirect to img page
        return redirect(url_for('admin.list_images'))

    # load img template
    return render_template('admin/images/image.html', action="Add",
                           add_img=add_img, form=form,
                           title="Add Img")


@admin.route('/images/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_img(id):
    """
    Edit a img
    """

    add_img = False

    img = Img.query.get_or_404(id)
    form = ImgForm(obj=img)
    if form.validate_on_submit():
        img.name = form.name.data
        db.session.commit()
        flash('You have successfully edited the img.')

        # redirect to the images page
        return redirect(url_for('admin.list_images'))

    form.name.data = img.name
    return render_template('admin/images/image.html', action="Edit",
                           add_img=add_img, form=form,
                           img=img, title="Edit Img")


@admin.route('/images/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_img(id):
    """
    Delete a img from the database
    """

    img = Img.query.get_or_404(id)
    db.session.delete(img)
    db.session.commit()
    flash('You have successfully deleted the img.')

    # redirect to the imgs page
    return redirect(url_for('admin.list_images'))

# app/admin/views.py


@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))


# app/admin/views.py


@admin.route('/users')
@login_required
def list_users():
    """
    List all users
    """
    check_admin()

    users = User.query.all()
    return render_template('admin/users/users.html',
                           users=users, title='Users')


@admin.route('/users/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_user(id):
    """
    Assign an image and a role to a user
    """
    check_admin()

    user = User.query.get_or_404(id)

    # prevent admin from being assigned a department or role
    if user.is_admin:
        abort(403)

    form = UserAssignForm(obj=user)
    if form.validate_on_submit():
        user.department = form.img.data
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('You have successfully assigned an img and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_users'))

    return render_template('admin/users/user.html',
                           user=user, form=form,
                           title='Assign User')
