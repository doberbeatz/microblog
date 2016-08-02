#!flaskenv/bin/python
from app import app
import os
app.run(debug=bool(os.environ.get('DEBUG')))
