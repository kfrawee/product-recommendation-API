from marshmallow import Schema, fields, validate

from .constants import (
    USER_GENDER_MAPPING,
    USER_SEGMENT_MAPPING,
    USER_RELATIONSHIP_MAPPING,
    USER_ACTIVITY_MAPPING,
)

DEFAULT_STRING_KWARGS = {
    "validate": [validate.Predicate("isascii"), validate.Length(min=1)]
}


class CreatePredictSchema(Schema):
    age = fields.Integer(required=True, validate=validate.Range(min=18, max=100))
    gender = fields.String(
        required=True, validate=validate.OneOf(USER_GENDER_MAPPING.values())
    )
    country_code = fields.String(validate=validate.Length(min=2, max=2), missing="ES")
    city = fields.String(**DEFAULT_STRING_KWARGS, missing="MADRID")
    seniority = fields.Integer(required=True, validate=validate.Range(min=0, max=720))
    segment = fields.String(
        required=True, validate=validate.OneOf(USER_SEGMENT_MAPPING.values())
    )
    relationship_type = fields.String(
        required=True, validate=validate.OneOf(USER_RELATIONSHIP_MAPPING.values())
    )
    activity_level = fields.String(
        required=True, validate=validate.OneOf(USER_ACTIVITY_MAPPING.values())
    )
    income = fields.Float(required=True, validate=validate.Range(min=0, max=1000000))


class PredictResponseSchema(Schema):
    """For response (Create Or Get) dump/order only"""

    invocation_id = fields.String()
    invocation_status = fields.String()
    created_on = fields.String()
    updated_on = fields.String()
    predictions = fields.List(fields.String())
    payload = fields.Dict()
    error = fields.Dict()

    class Meta:
        ordered = True
