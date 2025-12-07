#========================================
# GERENCIADOR DE FINAÇAS - Imports
# ========================================

from flask import Flask, jsonify, session, render_template, redirect, url_for, request, flash
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
    return render_template('index.html')

@app.get('/homepage')
def homepage():
    """Gerenciador de tarefas"""
    salario = getSalario()
    if 'id_session' not in session:
        return render_template('index.html')
    
    return render_template('homepage.html', salario = salario)

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
                SELECT id, username FROM users WHERE username = ? AND password = ?
                """,(userInput, passwordInput) )
    
    user = cur.fetchone()
        
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

@app.route('/demandas') #rota pra colocar as demandas financeiras na página 
def criarDemanda():
    conn = get_conn()
    cur = conn.cursor()
    
    cur.execute("""
                SELECT id, tipoDemanda, valopr FROM demandas ORDER BY ID """) 
    dados = cur.fetchall() #retorna as tuplas 
    conn.close()
    
# ========================================
# INICIALIZAÇÃO
# ========================================

if __name__ == '__main__':
    app.run(debug=True)