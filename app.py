from flask import Flask, jsonify, session, render_template, redirect, url_for, request
from datetime import datetime, timezone
import os
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))



@app.route('/')
def index():
    """Página de entrada para o site"""
    return render_template('index.html')

@app.get('/login')
def login():
    """Página de entrada para o site"""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)