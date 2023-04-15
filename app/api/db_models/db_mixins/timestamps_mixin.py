from datetime import datetime

from app.api.db_models import db


class TimestampMixin(object):
    created_on = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_on = db.Column(db.DateTime, onupdate=datetime.utcnow, nullable=True)
