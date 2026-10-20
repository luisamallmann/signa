from flask import request, redirect, url_for, render_template, session
from database.conexao import conexao


def _buscar_usuario():
    """Retorna (nome, email) do usuário logado ou None se não houver sessão."""
    user_id = session.get('user_id')
    if not user_id:
        return None

    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT name, email FROM users WHERE id = %s", (user_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    return usuario


def perfil():
    usuario = _buscar_usuario()
    if not usuario:
        return redirect(url_for('auth.fazer_login'))

    nome, email = usuario
    return render_template('perfil.html', nome=nome, email=email)


def editar_perfil():
    usuario = _buscar_usuario()
    if not usuario:
        return redirect(url_for('auth.fazer_login'))

    nome, email = usuario

    if request.method == 'GET':
        return render_template('editar-perfil.html', nome=nome, email=email)

    novo_nome = request.form['nome'].strip()

    if not novo_nome:
        return render_template('editar-perfil.html', nome=nome, email=email,
                               erro="O nome não pode ficar vazio")

    conn = conexao()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = %s WHERE id = %s",
                   (novo_nome, session['user_id']))
    conn.commit()
    cursor.close()
    conn.close()

    return render_template('editar-perfil.html', nome=novo_nome, email=email,
                           sucesso="Perfil atualizado com sucesso!")


def sair():
    session.clear()
    return redirect(url_for('home'))
