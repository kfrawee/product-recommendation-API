from datetime import datetime, timezone

import ulid

from app.api.db_models import db
from app.api.db_models.db_mixins import InvocationStatus

from .db_mixins import TimestampMixin


class Invocation(db.Model, TimestampMixin):
    __tablename__ = "invocation"

    invocation_id = db.Column(
        db.String(26),
        primary_key=True,
        default=lambda: str(ulid.from_timestamp(datetime.now(timezone.utc))),
    )
    invocation_status = db.Column(db.Enum(InvocationStatus), nullable=True)
    predictions = db.Column(
        db.JSON,
        nullable=True,
        comment="JSON representation of the predictions",
    )
    payload = db.Column(
        db.JSON,
        nullable=False,
        comment="JSON representation of the payload",
    )

    def __repr__(self):
        return f"<Invocation {self.invocation_id}>"

    def to_json(self):
        return {
            "invocation_id": self.invocation_id,
            "invocation_status": self.invocation_status.value,
            "created_on": self.created_on,
            "updated_on": self.updated_on,
            "predictions": self.predictions,
            "payload": self.payload,
        }
