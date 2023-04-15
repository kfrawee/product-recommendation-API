from flask_appbuilder import SQLA

db = SQLA()

Base = db.Model

from .invocations import Invocation
