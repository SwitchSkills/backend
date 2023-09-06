import json
from functools import wraps

from flask import g

from codebase_backend import logger


def catch_sever_crash(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise e
            logger.error(f"{g.execution_id} \n SERVER ERROR {e}")
            return json.dumps(
                {
                    'code': 500,
                    'message': f"following server error: {e}"
                }
            )

    return decorated_function
