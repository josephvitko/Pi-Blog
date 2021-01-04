from flask import Blueprint, render_template, request, flash, url_for, redirect
from flaskblog import db
from flaskblog.models import User, Role, UserRoles, Post
from flaskblog.admin.forms import RoleForm, SensorForm
from flaskblog.permissions import admin_permission
from flaskblog.weather_data.models import Sensor, Data

admin = Blueprint('admin', __name__)


@admin.route('/admin')
@admin_permission.require(http_exception=403)
def admin_dashboard():
    return render_template('admin_dashboard.html')


@admin.route('/admin/db/createall', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def createall():
    db.create_all()
    flash('Database models created', "success")
    return redirect(url_for('admin.admin_dashboard'))


@admin.route('/admin/db/dropall')
@admin_permission.require(http_exception=403)
def dropall():
    db.drop_all()
    flash('Database data dropped', "success")
    return redirect(url_for('admin.admin_dashboard'))


@admin.route('/admin/posts')
@admin_permission.require(http_exception=403)
def getposts():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=25)
    return render_template('admin_posts_dashboard.html', posts=posts, page=page, page_context='admin.getposts')


@admin.route('/admin/posts/<int:id>')
@admin_permission.require(http_exception=403)
def viewpost(id):
    post = Post.query.filter_by(id=id).first()
    return str(post)


@admin.route('/admin/posts/<int:id>/remove')
@admin_permission.require(http_exception=403)
def removepost(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Post deleted', 'success')
    return redirect(url_for('admin.getposts'))


@admin.route('/admin/roles', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def getroles():
    form = RoleForm()
    if form.validate_on_submit():
        return redirect(url_for('admin.newrole', name=form.name.data))
    roles = Role.query.paginate(per_page=25)
    return render_template('admin_roles_dashboard.html', roles=roles, form=form, page_context='admin.getroles')


@admin.route('/admin/roles/new/<string:name>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def newrole(name):
    nr = Role(name=name)
    db.session.add(nr)
    db.session.commit()
    flash('Role has been created', 'success')
    return redirect(url_for('admin.getroles'))


@admin.route('/admin/roles/drop/<string:name>')
@admin_permission.require(http_exception=403)
def droprole(name):
    Role.query.filter_by(name=name).delete()
    db.session.commit()
    flash('Role has been dropped', 'success')
    return redirect(url_for('admin.getroles'))


@admin.route('/admin/users')
@admin_permission.require(http_exception=403)
def getusers():
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id.asc()).paginate(per_page=25)
    return render_template('admin_users_dashboard.html', users=users, page=page, page_context='admin.getusers')


@admin.route('/admin/users/<string:user>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def viewuser(user):
    user = User.query.filter_by(username=user).first()
    roles = Role.query.all()
    form = RoleForm()
    if form.validate_on_submit():
        return redirect(url_for('admin.assignrole', role=form.name.data, user=user.username))
    return render_template('admin_user_dashboard.html', user=user, roles=roles, form=form)


@admin.route('/admin/users/<string:user>/roles')
@admin_permission.require(http_exception=403)
def viewroles(user):
    user = User.query.filter_by(username=user).first()
    return str(user.roles)


@admin.route('/admin/users/<string:user>/posts')
@admin_permission.require(http_exception=403)
def getuserposts(user):
    user = User.query.filter_by(username=user).first()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.date_posted.desc()).paginate(per_page=25)
    return render_template('admin_posts_dashboard.html', posts=posts, page=page, page_context='admin.getposts')


@admin.route('/admin/users/<string:user>/roles/assign/<string:role>', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
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
@admin_permission.require(http_exception=403)
def revokerole(user, role):
    user = User.query.filter_by(username=user).first()
    role = Role.query.filter_by(name=role).first()
    user.roles.remove(role)
    db.session.commit()
    flash('Role has been revoked', 'success')
    return redirect(url_for('admin.viewuser', user=user.username))


@admin.route('/admin/sensors', methods=['GET', 'POST'])
@admin_permission.require(http_exception=403)
def getsensors():
    form = SensorForm()
    if form.validate_on_submit():
        sensor = Sensor(name=form.name.data, unit=form.unit.data)
        db.session.add(sensor)
        db.session.commit()
        flash('Sensor created', 'success')
        return redirect(url_for('admin.getsensors'))
    sensors = Sensor.query.paginate(per_page=25)
    page = request.args.get('page', 1, type=int)
    return render_template('admin_sensors_dashboard.html', sensors=sensors, page=page, form=form, page_context='admin.getsensors')


@admin.route('/admin/sensors/<string:sensor>')
@admin_permission.require(http_exception=403)
def getsensordata(sensor):
    sensor = Sensor.query.filter_by(name=sensor).first()
    data = Data.query.filter_by(sensor_id=sensor.id).order_by(Data.date_recorded.desc()).paginate(per_page=50)
    page = request.args.get('page', 1, type=int)
    return render_template('admin_data_dashboard.html', data=data, sensor=sensor, page=page, page_context='admin.getsensordata')


@admin.route('/admin/sensors/<string:sensor>/delete')
@admin_permission.require(http_exception=403)
def deletesensor(sensor):
    sensor = Sensor.query.filter_by(name=sensor).first()
    Data.query.filter_by(sensor_id=sensor.id).delete()
    Sensor.query.filter_by(name=sensor.name).delete()
    db.session.commit()
    flash('Sensor has been deleted', 'success')
    return redirect(url_for('admin.getsensors'))


@admin.route('/admin/sensors/<string:sensor>/<int:id>/delete')
@admin_permission.require(http_exception=403)
def deletesensordatum(id, sensor):
    Data.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Datum has been deleted', 'success')
    return redirect(url_for('admin.getsensordata', sensor=sensor))


@admin.route('/admin/sensors/<string:sensor>/clear')
@admin_permission.require(http_exception=403)
def clearsensordata(sensor):
    sensor = Sensor.query.filter_by(name=sensor).first()
    Data.query.filter_by(sensor_id=sensor.id).delete()
    db.session.commit()
    flash('Data has been cleared', 'success')
    return redirect(url_for('admin.getsensordata', sensor=sensor))
