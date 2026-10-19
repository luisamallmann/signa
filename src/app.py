from flask import Flask, render_template
from routes.auth import auth
from routes.translator import translator

app = Flask(__name__)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(translator, url_prefix='/api')

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

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False) #evitar carregar 2x o modelo
