#========================================
# GERENCIADOR DE FINAÇAS - Imports
# ========================================

from flask import Flask, jsonify, session, render_template, redirect, url_for, request
from datetime import datetime, timezone
import os
import secrets
import sqlite3
from queryExecutor import get_conn

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))

# ========================================
# GERENCIADOR DE FINANÇAS - Rota de paginas
# ========================================

@app.route('/')
def index():
    """Página de entrada para o site"""
    return render_template('index.html')


@app.get('/homepage')
def homepage():
    """Gerenciador de tarefas"""
    return render_template('homepage.html')

# ========================================
# GERENCIADOR DE FINANÇAS - Rota de login
# ========================================

@app.post('/login_user')
def login():
    """login dos usuários"""
    userInput = request.form.get('nome', '').strip()
    passwordInput = request.form.get('senha', '').strip()
    
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
                SELECT username, password FROM users WHERE username = ? AND password = ?
                """,(userInput, passwordInput) )
    
    user = cur.fetchone()
    
    if user is None:
        return redirect(url_for('index', msg='Usuário não existe.'))    
    
    session['username'] = user['username']
    return redirect(url_for('homepage'))


# ========================================
# INICIALIZAÇÃO
# ========================================

if __name__ == '__main__':
    app.run(debug=True)