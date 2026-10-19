from flask import Blueprint
from controllers.translator_controllers import predict

translator = Blueprint('translator', __name__)

@translator.route('/predict', methods=['POST'])
def prever():
    return predict()