import os

from codebase_backend import app, DEBUG

if __name__ == '__main__':
    app.run(debug=DEBUG, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

