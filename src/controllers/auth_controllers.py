from flask import request, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from database.conexao import conexao

def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    email = request.form['email']
    senha = request.form['senha']

    conn = conexao()
    cursor = conn.cursor()

    sql = "SELECT * FROM users WHERE email = %s"

    valores = (email,)
    cursor.execute(sql,valores)

    resultado = cursor.fetchone()

    if resultado:
        if check_password_hash(resultado[3], senha):
            return redirect(url_for('home'))
        else:
            return render_template('login.html', erro_senha="Senha incorreta")
    else:
        return render_template('login.html', erro_email="Email não encontrado")

def cadastro():
    if request.method == 'GET':
        return render_template('cadastro.html')
    
    nome = request.form['nome']
    email = request.form['email']
    senha1 = request.form['senha1']
    senha2 = request.form['senha2']

    if senha1 != senha2:
        return render_template('cadastro.html', erro_senha="As senhas não coincidem")
    
    senha_hash = generate_password_hash(senha1)

    conn = conexao()
    cursor = conn.cursor()

    sql = "SELECT * FROM users WHERE email = %s"
    cursor.execute(sql,(email,))

    resultados = cursor.fetchall()

    if len(resultados) > 0:
        cursor.close()
        conn.close()
        return render_template('cadastro.html', erro_email="Email já cadastrado")
    
    sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    valores = (nome, email, senha_hash)

    cursor.execute(sql, valores)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('home.html'))