from http import HTTPStatus
from flask_appbuilder.api import BaseApi
from flask import request
from flask_appbuilder import expose
import logging
import json
from flask_appbuilder.security.decorators import protect
from app.api.ml_models import load_model

logger = logging.getLogger(__name__)
model = load_model()


class PredictAPIView(BaseApi):
    resource_name = "predict"

    @expose("/", methods=["POST"])
    # @protect()
    def post_predict_handler(self, *args, **kwargs):
        data = request.get_json()
        logger.debug(f"Received payload: {data}")

        return self.response(code=HTTPStatus.OK, message=data)

    @expose("/<invocation_id>", methods=["GET"])
    # @protect()
    def get_predict_handler(self, *args, **kwargs):
        invocation_id = kwargs.get("invocation_id")
        return self.response(code=HTTPStatus.OK, message=invocation_id)

    @expose("/<invocation_id>", methods=["DELETE"])
    @protect()
    def delete_predict_handler(self, *args, **kwargs):
        invocation_id = kwargs.get("invocation_id")
        return self.response(code=HTTPStatus.OK, message=invocation_id)

    @expose("/", methods=["GET"])
    # @protect()
    def list_predict_handler(self, *args, **kwargs):
        # invocation_id = kwargs.get("invocation_id");
        return self.response(
            code=HTTPStatus.OK, message={"predictions": [{"invocation_id": "123"}]}
        )
