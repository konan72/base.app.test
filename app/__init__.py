"""

by KoNaN 

"""
import os, sys
import threading
import jwt

from threading 							import Thread 
from flask 								import Flask, jsonify
from flask_restful 						import Api
from flask_sqlalchemy 					import SQLAlchemy
from flask_cors 						import CORS
from flask_compress 					import Compress
from werkzeug.middleware.proxy_fix 		import ProxyFix
from config								import app_config

from .commands 							import register_commands
from .utils 							import Logging

api 									= Api()
cors 									= CORS()
db 										= SQLAlchemy()
compress 								= Compress()
log 									= Logging()


def configure_extensions(app):
	try:
		with app.app_context():				
			compress.init_app(app)
			db.init_app(app)
			api.init_app(app)
			cors.init_app(app)
			log.init_app(app)
	
	except Exception as e:
		raise e


def create_app(configure=app_config['development']):
	try:    
		app 			= Flask(__name__, 
								instance_relative_config=False,
								static_url_path='', 
								template_folder='../templates', 
								static_folder="../static"
								)
		
		app.wsgi_app 	= ProxyFix(app.wsgi_app)

		if configure is not None:
			app.config.from_object(configure)
			configure_extensions(app)
			register_commands(app, db)			


	except Exception as e:
		app.logger.error(f"Error in create_app : {e}")
		raise e
	finally:
		return app


from .routes    import *
