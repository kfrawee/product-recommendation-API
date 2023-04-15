import logging
from datetime import datetime, timezone
from http import HTTPStatus
from typing import Dict

import numpy as np
import ulid
import xgboost as xgb
from flask import request
from flask_appbuilder import expose
from flask_appbuilder.api import BaseApi
from flask_appbuilder.security.decorators import protect
from marshmallow import ValidationError

from app import db
from app.api.db_models import Invocation
from app.api.db_models.db_mixins import InvocationStatus
from app.api.ml_models import load_model, processData, target_cols
from app.api.views import (BASE_USER_DATA_TEMPLATE, INPUT_MAPPING,
                           PRODUCTS_MAPPINGS, USER_ACTIVITY_MAPPING,
                           USER_GENDER_MAPPING, USER_RELATIONSHIP_MAPPING,
                           USER_SEGMENT_MAPPING, CreatePredictSchema,
                           PredictResponseSchema, convert_values_to_string,
                           translate_keys_or_values)

logger = logging.getLogger(__name__)
model = load_model()
create_predict_schema = CreatePredictSchema()
predict_response_schema = PredictResponseSchema()


def prepare_data(data: Dict) -> Dict:
    """
    Cleaning input data
    Translate keys to match the model input
    :param data:
    :return:
    data: Dict
    """
    #  translate keys
    data = translate_keys_or_values(data, INPUT_MAPPING, keys=True, reverse=True)
    # translate values
    data = translate_keys_or_values(
        data, USER_SEGMENT_MAPPING, keys=False, reverse=True
    )
    data = translate_keys_or_values(
        data,
        USER_ACTIVITY_MAPPING,
        keys=False,
        translate_only="ind_actividad_cliente",
        reverse=True,
    )
    data = translate_keys_or_values(
        data,
        USER_RELATIONSHIP_MAPPING,
        keys=False,
        translate_only="tiprel_1mes",
        reverse=True,
    )
    data = translate_keys_or_values(data, USER_GENDER_MAPPING, keys=False, reverse=True)

    # convert values to string
    data = convert_values_to_string(data)
    return data


class PredictAPIView(BaseApi):
    base_route = "predict"

    @expose("/", methods=["POST"])
    def post_predict_handler(self, *args, **kwargs):
        data = request.get_json()
        # validate data
        try:
            data = create_predict_schema.load(data)
        except ValidationError as err:
            logger.warning(f"Received invalid data: {data}")
            return (
                {"error": err.messages},
                HTTPStatus.BAD_REQUEST,
            )

        logger.debug(f"Received valid data: {data}")


        try:
            # create invocation record
            invocation_id = str(ulid.from_timestamp(datetime.now(timezone.utc)))
            invocation = Invocation(
                invocation_id=invocation_id,
                invocation_status=InvocationStatus.STARTED,
                payload=data,
            )
            db.session.add(invocation)
            db.session.commit()
            prepared_data = prepare_data(data)
            logger.debug(f"Prepared data: {prepared_data}")

            # update input
            user_data = BASE_USER_DATA_TEMPLATE.copy()
            user_data.update(prepared_data)
            logger.debug(f"User input data to model: {user_data}")

            x_vars_list, y_vars_list, cust_dict = processData(
                in_file_name=[user_data], cust_dict=dict(), data_input=True
            )
            del y_vars_list, cust_dict

            # Update Status
            invocation.invocation_status = InvocationStatus.RUNNING
            db.session.commit()

            x = np.array(x_vars_list)
            xgx = xgb.DMatrix(x)
            preds = model.predict(xgx)
            preds = np.argsort(preds, axis=1)
            preds = np.fliplr(preds)[:, :7]
            # flatten preds
            if preds.shape[0] == 1:
                preds = preds.flatten()
            preds = ["".join(list(target_cols[pred])) for pred in preds]

            # translate predictions
            final_predictions = translate_keys_or_values(preds, PRODUCTS_MAPPINGS)
            logger.debug(f"Predictions: {final_predictions}")

            # Update Status
            invocation.invocation_status = InvocationStatus.COMPLETED
            invocation.predictions = final_predictions
            db.session.commit()

            return predict_response_schema.dump(invocation.to_json()), HTTPStatus.OK
        except Exception as e:
            import traceback

            invocation.invocation_status = InvocationStatus.FAILED
            invocation.error = {"error": str(e), "traceback": traceback.format_exc()}
            db.session.commit()

            logger.exception(f"Error in predict handler: {str(e)}")
            return {
                "error": "Internal Server Error",
            }, HTTPStatus.INTERNAL_SERVER_ERROR

    @expose("/<invocation_id>", methods=["GET"])
    def get_predict_handler(self, *args, **kwargs):
        try:
            invocation_id = kwargs.get("invocation_id")

            session = db.session
            query = session.query(Invocation)
            query = query.filter(Invocation.invocation_id == invocation_id)
            invocation = query.one_or_none()
            if invocation is None:
                return {
                    "error": f"Invocation {invocation_id} not found"
                }, HTTPStatus.NOT_FOUND

            logger.debug(f"Found invocation: {invocation}")
            return predict_response_schema.dump(invocation.to_json()), HTTPStatus.OK
        except Exception as e:
            logger.exception(f"Error in get handler: {str(e)}")
            return {"error": "Internal Server Error"}, HTTPStatus.INTERNAL_SERVER_ERROR

    @expose("/<invocation_id>", methods=["DELETE"])
    @protect()
    def delete_predict_handler(self, *args, **kwargs):
        try:
            invocation_id = kwargs.get("invocation_id")

            session = db.session
            query = session.query(Invocation)
            query = query.filter(Invocation.invocation_id == invocation_id)
            invocation = query.one_or_none()
            if invocation is None:
                return {
                    "error": f"Invocation {invocation_id} not found"
                }, HTTPStatus.NOT_FOUND

            logger.debug(f"Found invocation: {invocation}")
            session.delete(invocation)

            session.commit()
            return {}, HTTPStatus.NO_CONTENT
        except Exception as e:
            logger.exception(f"Error in delete handler: {str(e)}")
            return {"error": "Internal Server Error"}, HTTPStatus.INTERNAL_SERVER_ERROR

    @expose("/", methods=["GET"])
    def list_predict_handler(self, *args, **kwargs):
        try:
            session = db.session
            query = session.query(Invocation)
            invocations = query.all()
            logger.debug(f"Found {len(invocations)} invocations")
            return {
                "count": len(invocations),
                "invocations": [invocation.to_json() for invocation in invocations],
            }, HTTPStatus.OK
        except Exception as e:
            logger.exception(f"Error in list handler: {str(e)}")
            return {"error": "Internal Server Error"}, HTTPStatus.INTERNAL_SERVER_ERROR
