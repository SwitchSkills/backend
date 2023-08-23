import json
from functools import wraps

from flask import g

from app import logger


def catch_sever_crash(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(g.execution_id, "SERVER ERROR", e)
            return json.dumps(
                {
                    'code': 500,
                    'message': f"following key error: {e}"
                }
            )
    return decorated_function
