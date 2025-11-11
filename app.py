from flask import Flask, jsonify, session
from datetime import datetime, timezone
import os
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))



app.run(debug=True)