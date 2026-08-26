from flask import Blueprint
from controllers.auth_controllers import login, cadastro

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def fazer_login():
    return login()

@auth.route('/cadastro', methods=['GET', 'POST'])
def fazer_cadastro():
    return cadastro()

@auth.route('/alterar-senha', methods=['GET', 'POST'])
def alterar_senha():
    return alt_senha()

@auth.route('/alterar-email', methods=['GET', 'POST'])
def alterar_email():
    return alt_email()

# fazer funcoes de alterar senha e alterar email
