from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

#autoriser le cors uniquement sur l'url local de react
CORS(app, origins=["http://localhost:5173"])



@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
