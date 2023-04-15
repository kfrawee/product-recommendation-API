from marshmallow import Schema, fields
from marshmallow_union import Union


class EventDetails(Schema):
    name = fields.String()


class FailedEventDetails(Schema):
    error = fields.String()
    cause = fields.String()


class ExecutionHistoryEventSchema(Schema):
    class Meta:
        ordered = True

    type = fields.String()
    timestamp = fields.String()
    stateEnteredEventDetails = fields.Nested(EventDetails)
    stateExitedEventDetails = fields.Nested(EventDetails)
    lambdaFunctionFailedEventDetails = fields.Nested(FailedEventDetails)


class TranslationLogsLanguageDefinitionSchema(Schema):
    class Meta:
        ordered = True

    format = fields.String()
    type = fields.String()
    original_presigned_url = fields.String()


class TranslationLogsSchema(Schema):
    class Meta:
        ordered = True

    transaction_id = fields.String()
    response_collection_id = fields.String()
    invocation_id = fields.String()
    invocation_status = fields.String()
    from_language = fields.String()
    to_language = fields.String()
    started_on = fields.String()
    finished_on = fields.String()
    elapsed_time = fields.Float()
    translation_steps_breakdown = fields.Dict()
    obfuscated_data_url = fields.String()
    obfuscated_processed_data_url = fields.String()
    from_language_definition = Union(fields=[fields.Dict(), fields.String()])
    to_language_definition = Union(fields=[fields.Dict(), fields.String()])
    translation_rules_url = fields.String()
    translation_ruleset_url = fields.String()
    post_translation_rules_url = fields.String()
    post_translation_ruleset_url = fields.String()
    graph_data_url = fields.String()
    callback_url = fields.String()
    translation_internal_status = fields.Dict()
    warnings = fields.Dict()
    failure_reason = fields.String()
