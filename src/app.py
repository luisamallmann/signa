from flask import Flask, render_template, request, session, redirect, url_for
from routes.auth import auth
from routes.translator import translator
from routes.perfil import perfil_bp

app = Flask(__name__)
app.secret_key = "signa-feciti-2026"  # necessário para guardar quem está logado (session)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(translator, url_prefix='/api')
app.register_blueprint(perfil_bp, url_prefix='/perfil')


# avisa o header.js (que roda no navegador) se tem alguém logado
@app.after_request
def sincronizar_cookie_login(resposta):
    if session.get('user_id'):
        resposta.set_cookie('signa_logado', '1', samesite='Lax')
    elif request.cookies.get('signa_logado'):
        resposta.delete_cookie('signa_logado')
    return resposta

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/como-funciona', methods=['GET'])
def cf():
    return render_template('como-funciona.html')

@app.route('/tradutor', methods=['GET'])
def trad():
    return render_template('tradutor.html')

@app.route('/sobre', methods=['GET'])
def sobre():
    return render_template('sobre.html')

@app.route('/contato', methods=['GET'])
def contato():
    return render_template('contato.html')

@app.route('/configuracoes', methods=['GET'])
def configuracoes():
    usuario = _buscar_usuario()
    if not usuario:
        return redirect(url_for('auth.fazer_login'))
    nome, email = usuario
    return render_template('configuracoes.html', nome=nome, email=email)

@app.route('/privacidade', methods=['GET'])
def privacidade():
    return render_template('privacidade.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False) #evitar carregar 2x o modelo
