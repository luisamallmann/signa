from flask import Flask, render_template
from routes.auth import auth

app = Flask(__name__)

app.register_blueprint(auth, url_prefix='/auth')

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)