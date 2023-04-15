"""
`CONTEXT_ENV` is an environmental specified in this project's docker container at runtime.
It is used to determine in which context the backend server is running in.
If `CONTEXT_ENV` is not defined (or "dev"), then this must be a local/dev environment.
"""
import os
from enum import Enum


class EnvTypes(Enum):
    DEV = "DEV"
    PROD = "PROD"
    STAGE = "STAGE"
    TEST = "TEST"


def get_env() -> EnvTypes:
    if os.environ.get("CONTEXT_ENV") is None:
        return EnvTypes.DEV.value
    else:
        return EnvTypes(os.environ.get("CONTEXT_ENV")).value


def is_dev() -> bool:
    return get_env() == EnvTypes.DEV.value
