from flask import Blueprint
from controllers.perfil_controllers import perfil, editar_perfil, sair

# o Blueprint se chama perfil_bp para não apagar a função perfil() importada acima
perfil_bp = Blueprint('perfil', __name__)

@perfil_bp.route('/', methods=['GET'])
def ver_perfil():
    return perfil()

@perfil_bp.route('/editar', methods=['GET', 'POST'])
def editar():
    return editar_perfil()

@perfil_bp.route('/sair', methods=['GET'])
def logout():
    return sair()
