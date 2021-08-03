
# TODO: set FLASK_APP=nameofthefile.py
# TODO: set FLASK_ENV=development
# FLASK RUN

from frontend.app import app
from frontend import routes


if __name__ == "__main__":
    app.run(debug=True)
