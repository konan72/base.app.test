import os
import logging
from logging.handlers import RotatingFileHandler


class Logging(object):

	def __init__(self, app=None):
		if app:
			self.init_app(app)

	def init_app(self, app):

		if not os.path.exists(app.config['LOGS']):
			os.makedirs(app.config['LOGS'])
			
		self.info_file 		= os.path.join(app.config['LOGS'], 'info.log')
		self.debug_file 	= os.path.join(app.config['LOGS'], 'debug.log')
		self.error_file 	= os.path.join(app.config['LOGS'], 'error.log')

		self.formatter 		= logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]' )
		
		self.rfh1 			= RotatingFileHandler(self.info_file, maxBytes=1000000, backupCount=10)
		self.rfh2 			= RotatingFileHandler(self.debug_file, maxBytes=1000000, backupCount=10)
		self.rfh3 			= RotatingFileHandler(self.error_file, maxBytes=1000000, backupCount=10)
		
		self.rfh1.setLevel(logging.INFO)
		self.rfh1.setFormatter(self.formatter)

		self.rfh2.setLevel(logging.DEBUG)
		self.rfh2.setFormatter(self.formatter)

		self.rfh3.setLevel(logging.ERROR)
		self.rfh3.setFormatter(self.formatter)

		app.logger.addHandler(self.rfh1)
		app.logger.addHandler(self.rfh2)
		app.logger.addHandler(self.rfh3)
