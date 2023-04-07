from flask import Flask

from flask_restful import Api

from server.chatgpt import ChatGPT

from logging.config import dictConfig


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
api = Api(app)

api.add_resource(ChatGPT, '/chatgpt')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/prompt', methods=['GET', 'POST'])
def prompt():
    return "cc"


if __name__ == '__main__':
    app.run(debug=True)
