import json
import time
import uuid
from flask import g, request

from codebase_backend import app, logger
from config import version


@app.after_request
def after_request(response):
    if response and response.get_json():
        data = response.get_json()

        data["time_request"] = int(time.time())
        data["version"] = version.VERSION

        response.set_data(json.dumps(data))

    return response


@app.before_request
def before_request_func():
    execution_id = uuid.uuid4()
    g.start_time = time.time()
    g.execution_id = execution_id

    logger.info(f"id: {g.execution_id}\n ROUTE CALLED {request.url}")