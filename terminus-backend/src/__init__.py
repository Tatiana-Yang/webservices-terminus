from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="http://localhost:8080")

def create_app(debug=False):

	app = Flask(__name__)
	app.debug = debug
	app.config['appKeyTerminus'] = 'dsqyuiopi'
	#app.config['PORT'] = 80

	from .routes import routes
	app.register_blueprint(routes.bpapi)

	from .sockets import socket

	socketio.init_app(app)
	return app