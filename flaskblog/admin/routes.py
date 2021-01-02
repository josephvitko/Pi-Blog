from flask import Blueprint, render_template, request, flash, url_for, redirect
from flaskblog import db
from flaskblog.models import User, Role, UserRoles, Post
from flaskblog.admin.forms import RoleForm

admin = Blueprint('admin', __name__)


@admin.route('/admin')
def admin_dashboard():
    return render_template('admin_dashboard.html')


@admin.route('/admin/db/createall', methods=['GET', 'POST'])
def createall():
    db.create_all()
    flash('Database models created', "success")
    return redirect(url_for('admin.admin_dashboard'))


@admin.route('/admin/db/dropall')
def dropall():
    db.drop_all()
    flash('Database data dropped', "success")
    return redirect(url_for('admin.admin_dashboard'))


@admin.route('/admin/posts')
def getposts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=25)
    return render_template('admin_posts_dashboard.html', posts=posts, page=page, page_context='admin.getposts')


@admin.route('/admin/posts/<int:id>')
def viewpost(id):
    post = Post.query.filter_by(id=id).first()
    return str(post)


@admin.route('/admin/posts/<int:id>/remove')
def removepost(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Post deleted', 'success')
    return redirect(url_for('admin.getposts'))


@admin.route('/admin/roles', methods=['GET', 'POST'])
def getroles():
    form = RoleForm()
    if form.validate_on_submit():
        return redirect(url_for('admin.newrole', name=form.name.data))
    else:
        flash('Role is invalid', 'danger')
    roles = Role.query.paginate(per_page=25)
    return render_template('admin_roles_dashboard.html', roles=roles, form=form, page_context='admin.getroles')


@admin.route('/admin/roles/new/<string:name>', methods=['GET', 'POST'])
def newrole(name):
    nr = Role(name=name)
    db.session.add(nr)
    db.session.commit()
    flash('Role has been created', 'success')
    return redirect(url_for('admin.getroles'))


@admin.route('/admin/roles/drop/<string:name>')
def droprole(name):
    Role.query.filter_by(name=name).delete()
    db.session.commit()
    flash('Role has been dropped', 'success')
    return redirect(url_for('admin.getroles'))


@admin.route('/admin/users')
def getusers():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id.asc()).paginate(per_page=25)
    return render_template('admin_users_dashboard.html', users=users, page=page, page_context='admin.getusers')


@admin.route('/admin/users/<string:user>', methods=['GET', 'POST'])
def viewuser(user):
    user = User.query.filter_by(username=user).first()
    roles = Role.query.all()
    form = RoleForm()
    if form.validate_on_submit():
        return redirect(url_for('admin.assignrole', role=form.name.data, user=user.username))
    else:
        flash('Role is invalid', 'danger')
    return render_template('admin_user_dashboard.html', user=user, roles=roles, form=form)


@admin.route('/admin/users/<string:user>/roles')
def viewroles(user):
    user = User.query.filter_by(username=user).first()
    return str(user.roles)


@admin.route('/admin/users/<string:user>/posts')
def getuserposts(user):
    user = User.query.filter_by(username=user).first()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.date_posted.desc()).limit(25).all()
    return str(posts)


@admin.route('/admin/users/<string:user>/roles/assign/<string:role>', methods=['GET', 'POST'])
def assignrole(user, role):
    user = User.query.filter_by(username=user).first()
    role = Role.query.filter_by(name=role).first()
    if role is None:
        flash('Role does not exist', 'danger')
        return redirect(url_for('admin.viewuser', user=user.username))
    else:
        user.roles.append(role)
        db.session.commit()
        flash('Role assigned', 'success')
        return redirect(url_for('admin.viewuser', user=user.username))


@admin.route('/admin/users/<string:user>/roles/revoke/<string:role>')
def revokerole(user, role):
    user = User.query.filter_by(username=user).first()
    role = Role.query.filter_by(name=role).first()
    user.roles.remove(role)
    db.session.commit()
    flash('Role has been revoked', 'success')
    return redirect(url_for('admin.viewuser', user=user.username))
