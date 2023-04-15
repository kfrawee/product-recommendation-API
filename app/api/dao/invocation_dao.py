from app.api.db_models import Invocation
from app.api.dao import BaseDAO


class InvocationDAO(BaseDAO):
    model_cls = Invocation
