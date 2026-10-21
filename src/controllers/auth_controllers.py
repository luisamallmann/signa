from flask import request, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from database.conexao import conexao
from controllers import codigo_email

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
            session['user_id'] = resultado[0]  # guarda quem entrou
            cursor.close()
            conn.close()
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
    session['user_id'] = cursor.lastrowid  # já entra logado depois de cadastrar
    cursor.close()
    conn.close()

    return redirect(url_for('home'))

def _buscar(sql, valores):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute(sql, valores)
    linha = cursor.fetchone()
    cursor.close()
    conn.close()
    return linha


def _executar(sql, valores):
    conn = conexao()
    cursor = conn.cursor()
    cursor.execute(sql, valores)
    conn.commit()
    cursor.close()
    conn.close()


def _email_logado():
    if not session.get('user_id'):
        return None
    linha = _buscar("SELECT email FROM users WHERE id = %s", (session['user_id'],))
    return linha[0] if linha else None


def _codigo_digitado():
    return "".join(request.form.getlist('digito')).strip()


# ---------------- ALTERAR SENHA ----------------
# etapas: email -> codigo -> senha -> sucesso (guardadas na session)

def alt_senha():
    def tela(**extra):
        etapa = session.get('senha_etapa', 'email')
        email = session.get('senha_email') or _email_logado() or ''
        return render_template('alterar-senha.html', etapa=etapa, email=email,
                               logado=bool(session.get('user_id')),
                               expira_em=codigo_email.segundos_restantes('senha', email), **extra)

    if request.method == 'GET':
        if request.args.get('reiniciar') or session.get('senha_etapa') == 'sucesso':
            session.pop('senha_etapa', None)
            session.pop('senha_email', None)
        return tela()

    acao = request.form.get('etapa')

    if acao == 'email':
        email = request.form.get('email', '').strip()
        if not _buscar("SELECT id FROM users WHERE email = %s", (email,)):
            return tela(erro_email="Não existe conta com esse email.")
        session['senha_email'] = email
        session['senha_etapa'] = 'codigo'
        codigo_email.gerar_e_enviar('senha', email)
        return tela()

    email = session.get('senha_email')
    if not email:
        session.pop('senha_etapa', None)
        return tela()

    if acao == 'reenviar':
        codigo_email.gerar_e_enviar('senha', email)
        return tela(aviso="Enviamos um novo código.")

    if acao == 'codigo':
        erro = codigo_email.verificar('senha', email, _codigo_digitado())
        if erro:
            return tela(erro_codigo=erro)
        session['senha_etapa'] = 'senha'
        return tela()

    if acao == 'senha' and session.get('senha_etapa') == 'senha':
        senha1 = request.form.get('senha1', '')
        senha2 = request.form.get('senha2', '')
        if len(senha1) < 6:
            return tela(erro_senha="A senha precisa ter pelo menos 6 caracteres.")
        if senha1 != senha2:
            return tela(erro_senha="As senhas não coincidem.")
        _executar("UPDATE users SET password = %s WHERE email = %s",
                  (generate_password_hash(senha1), email))
        session['senha_etapa'] = 'sucesso'
        session.pop('senha_email', None)
        return tela()

    return tela()


# ---------------- ALTERAR EMAIL ----------------
# etapas: form -> codigo -> sucesso (precisa estar logado)

def alt_email():
    email_atual = _email_logado()
    if not email_atual:
        return redirect(url_for('auth.fazer_login'))

    def tela(**extra):
        etapa = session.get('email_etapa', 'form')
        novo = session.get('email_novo', '')
        return render_template('alterar-email.html', etapa=etapa, novo_email=novo,
                               expira_em=codigo_email.segundos_restantes('email', novo), **extra)

    if request.method == 'GET':
        if request.args.get('reiniciar') or session.get('email_etapa') == 'sucesso':
            session.pop('email_etapa', None)
            session.pop('email_novo', None)
        return tela()

    acao = request.form.get('etapa')

    if acao == 'form':
        atual = request.form.get('email_atual', '').strip()
        novo = request.form.get('novo_email', '').strip()
        senha = request.form.get('senha', '')
        valores = dict(form_atual=atual, form_novo=novo)
        if atual.lower() != email_atual.lower():
            return tela(erro="O email atual não confere com o da sua conta.", **valores)
        if not novo or novo.lower() == email_atual.lower():
            return tela(erro="Digite um email novo, diferente do atual.", **valores)
        if _buscar("SELECT id FROM users WHERE email = %s", (novo,)):
            return tela(erro="Esse email já está em uso por outra conta.", **valores)
        linha = _buscar("SELECT password FROM users WHERE id = %s", (session['user_id'],))
        if not linha or not check_password_hash(linha[0], senha):
            return tela(erro="Senha incorreta.", **valores)
        session['email_novo'] = novo
        session['email_etapa'] = 'codigo'
        codigo_email.gerar_e_enviar('email', novo)
        return tela()

    novo = session.get('email_novo')
    if not novo:
        session.pop('email_etapa', None)
        return tela()

    if acao == 'reenviar':
        codigo_email.gerar_e_enviar('email', novo)
        return tela(aviso="Enviamos um novo código.")

    if acao == 'codigo':
        erro = codigo_email.verificar('email', novo, _codigo_digitado())
        if erro:
            return tela(erro_codigo=erro)
        _executar("UPDATE users SET email = %s WHERE id = %s", (novo, session['user_id']))
        session['email_etapa'] = 'sucesso'
        return tela()

    return tela()
