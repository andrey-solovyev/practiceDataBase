from flask_admin import expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.utils import redirect

from ModelsDataBase import *
from __init__ import admin, db


class UserSiteView(ModelView):
    edit_modal = True

    # def is_accessible(self):
    #     if current_user.is_authenticated and current_user.role > 0:
    #         print(current_user)
    #         return True
    #     return False
    #
    # def not_auth(self):
    #     return "you are not auth"


admin.add_view(UserSiteView(Construction, db.session))
admin.add_view(UserSiteView(Construction_position, db.session))
admin.add_view(UserSiteView(Flat, db.session))
admin.add_view(UserSiteView(Contract, db.session))
admin.add_view(UserSiteView(Human, db.session))
admin.add_view(UserSiteView(Type_building, db.session))
