from flask import Flask

from flask_restful import Api

from server.chatgpt import ChatGPT
from server.xueqiu import XueQiu

from logging.config import dictConfig

from cmd import index as cmd_index

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
api.add_resource(XueQiu, '/openai/xueqiu')


app.register_blueprint(cmd_index.indexCmdBp)

if __name__ == '__main__':
    app.run(debug=True)
