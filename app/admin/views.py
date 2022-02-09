# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from . forms import ImgForm
from .. import db
from ..models import Img

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# Img Views

@admin.route('/images', methods=['GET', 'POST'])
@login_required
def list_images():
    """
    List all images
    """
    check_admin()

    images = Img.query.all()

    return render_template('admin/images/images.html',
                           images=images, title="images")

@admin.route('/images/add', methods=['GET', 'POST'])
@login_required
def add_img():
    """
    Add a image to the database
    """
    check_admin()

    add_img = True

    form = ImgForm()
    if form.validate_on_submit():
        img = Img(name=form.name.data, mimetype=form.mimetype.data)
        try:
            # add img to the database
            db.session.add(img)
            db.session.commit()
            flash('You have successfully added a new img.')
        except:
            # in case img name already exists
            flash('Error: img name already exists.')

        # redirect to imgs page
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
    check_admin()

    add_img = False

    img = Img.query.get_or_404(id)
    form = ImgForm(obj=img)
    if form.validate_on_submit():
        img.name = form.name.data
        img.description = form.mimetype.data
        db.session.commit()
        flash('You have successfully edited the img.')

        # redirect to the images page
        return redirect(url_for('admin.list_images'))

    form.mimetype.data = img.mimetype
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
    check_admin()

    img = Img.query.get_or_404(id)
    db.session.delete(img)
    db.session.commit()
    flash('You have successfully deleted the img.')

    # redirect to the imgs page
    return redirect(url_for('admin.list_imgs'))

    return render_template(title="Delete Img")
