from flask_principal import Permission, RoleNeed, identity_loaded
from flask import current_app


admin_permission = Permission(RoleNeed('admin'))
post_permission = Permission(RoleNeed('canPost'))
