from flask import Blueprint
from controllers.perfil_controllers import perfil, editar_perfil, sair

perfil = Blueprint('perfil', __name__)

@perfil.route('/', methods=['GET'])

def ver_perfil():
    return perfil()

@perfil.route('/editar', methods=['GET', 'POST'])
def editar():
    return editar_perfil()

@perfil.route('/sair', methods=['GET'])
def logout():
    return sair()
