#========================================
# GERENCIADOR DE FINAÇAS - Imports
# ========================================

from flask import Flask, jsonify, session, render_template, redirect, url_for, request, flash
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import secrets
import sqlite3
import time 
from queryExecutor import get_conn

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))

# ========================================
# GERENCIADOR DE FINANÇAS - Rota de paginas
# ========================================

@app.route('/')
def index():
    return render_template('index.html')

@app.get('/homepage')
def homepage():
    """Gerenciador de tarefas"""
    salario = getSalario()
    if 'id_session' not in session:
        return render_template('index.html')
    
    return render_template('homepage.html', salario = salario)

@app.route('/registro')
def registro():
    return render_template('criarConta.html')

# ========================================
# GERENCIADOR DE FINANÇAS - Rota de registro
# ========================================

@app.post('/registro')
def criarConta():
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip() 
        
        agora = int(time.time())
        
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
                    (username, email, password, agora))
        
        conn.commit()
        conn.close()
        return render_template('index.html')

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
    cur.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (userInput,))
    user = cur.fetchone()
    conn.close()
        
    if user is None:
        flash('Usuário ou senha incorreta.', 'danger')   # 'danger' = categoria (bootstrap)
        return redirect(url_for('index'))
        
    session['id_session'] = user['id']    
    session['username'] = user['username']
    return redirect(url_for('homepage'))

# ========================================
# GERENCIADOR DE FINANÇAS - Rota de salario
# ========================================

def getSalario():
    
    if 'id_session' not in session:
        return 0.00
    
#pegar o salario no banco de dados
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
                SELECT salario FROM users WHERE id = ?""",(session['id_session'],))
    salarioSession = cur.fetchone()

    conn.close()
    return salarioSession['salario']

@app.post('/attSalario')
def atualizarSalario():
#rota pra atualizar o salario 
    salario = int(request.form.get('salario', '').strip())
        
#comunicacao com o banco de dados    
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
                UPDATE users SET salario = ?
                WHERE id = ?
                """,(salario, session['id_session']) )
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('homepage'))

# ========================================
# GERENCIADOR DE FINANÇAS - Rota de demanda
# ========================================

@app.route('/demandas/criar') #rota pra colocar as demandas financeiras na página 
def criarDemanda():
    conn = get_conn()
    cur = conn.cursor()
    
    tipo = request.form.get('tipo', '').strip
    desc = request.form.get('desc', '').strip
    valor = request.form.get('valor', '').strip 
    
    agora = int(time.time)
    
    cur.execute("""
                INSERT INTO demandas (tipoDemanda, descricao, valor, data)
                VALUES (?, ?, ?, ?)""",
                (tipo, desc, valor, agora ))
     
    conn.commit
    conn.close()
    
    return redirect(url_for('homepage'))
    
@app.get('/demandas')
def mostrarDemanda():
    conn = get_conn()
    cur = conn.cursor()
    
    cur.execute ("""
                 SELECT id, tipoDemanda, descricao, valor, data
                 FROM demandas 
                 ORDER BY id
                 """)
    demandas = cur.fetchall()
    conn.close()
    
    return render_template('demandas.html', demandas=demandas)
    
# ========================================
# INICIALIZAÇÃO
# ========================================

if __name__ == '__main__':
    app.run(debug=True)