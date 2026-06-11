from flask import Blueprint
from controllers.auth_controllers import login, cadastro

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def fazer_login():
    return login()

@auth.route('/cadastro', methods=['GET', 'POST'])
def fazer_cadastro():
    return cadastro()
