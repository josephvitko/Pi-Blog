from flask import Blueprint
from flaskblog import db
from flaskblog.models import User, Role, UserRoles, Post

admin = Blueprint('admin', __name__)


@admin.route('/admin')
def admin_dashboard():
    pass


@admin.route('/admin/db/createall', methods=['GET', 'POST'])
def createall():
    db.create_all()
    return 'created all'


@admin.route('/admin/db/dropall')
def dropall():
    db.drop_all()
    return 'dropped all'


@admin.route('/admin/posts')
def getposts():
    return str(Post.query.order_by(Post.date_posted.desc()).limit(25).all())


@admin.route('/admin/posts/<int:id>')
def viewpost(id):
    post = Post.query.filter_by(id=id).first()
    return str(post)


@admin.route('/admin/posts/<int:id>/remove')
def removepost(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()
    return str('deleted post ' + str(id))


@admin.route('/admin/roles')
def getroles():
    roles = Role.query.all()
    return str(roles)


@admin.route('/admin/roles/new/<string:name>')
def newrole(name):
    nr = Role(name=name)
    db.session.add(nr)
    db.session.commit()
    return str(name + ' added')


@admin.route('/admin/roles/drop/<string:name>')
def droprole(name):
    Role.query.filter_by(name=name).delete()
    db.session.commit()
    return str(name + ' dropped')


@admin.route('/admin/users')
def getusers():
    users = User.query.limit(100).all()
    return str(users)


@admin.route('/admin/users/<string:user>')
def viewuser(user):
    user = User.query.filter_by(username=user).first()
    return str(user)


@admin.route('/admin/users/<string:user>/roles')
def viewroles(user):
    user = User.query.filter_by(username=user).first()
    return str(user.roles)


@admin.route('/admin/users/<string:user>/posts')
def getuserposts(user):
    user = User.query.filter_by(username=user).first()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.date_posted.desc()).limit(25).all()
    return str(posts)


@admin.route('/admin/users/<string:user>/roles/assign/<string:role>')
def assignrole(user, role):
    user = User.query.filter_by(username=user).first()
    role = Role.query.filter_by(name=role).first()
    user.roles.append(role)
    db.session.commit()
    return str(str(user) + ' assigned ' + str(role))


@admin.route('/admin/users/<string:user>/roles/revoke/<string:role>')
def revokerole(user, role):
    user = User.query.filter_by(username=user).first()
    role = Role.query.filter_by(name=role).first()
    user.roles.remove(role)
    db.session.commit()
    return str(str(role) + ' revoked from ' + str(user))
