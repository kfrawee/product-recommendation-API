import json
import uuid
from datetime import datetime, timezone

from sqlalchemy import orm

from app.api.db_models import db
from app.api.db_models.db_mixins import InvocationStatus

from .db_mixins import TimestampMixin, arr_loader, json_loader


class Invocation(db.Model, TimestampMixin):
    __tablename__ = "invocation"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    status = db.Column(db.Enum(InvocationStatus), nullable=True)
    labels = db.Column(
        db.JSON,
        nullable=True,
        default=dict,
        comment="JSON representation of the labels",
    )
    payload = db.Column(
        db.JSON,
        nullable=False,
        default=dict,
        comment="JSON representation of the payload",
    )
    error = db.Column(
        db.JSON,
        nullable=True,
        default=dict,
        comment="JSON representation of the error",
    )
