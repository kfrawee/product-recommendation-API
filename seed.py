import datetime
import json
import random
import ulid

import app


def seed():
    # seed random invocations data
    pass


if __name__ == "__main__":
    with app.app.app_context():
        seed()
