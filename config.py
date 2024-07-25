
import os




class DevelopmentConfig(object):
	"""
	Development configurations

	"""	
	NAME 							= 'Base.app'
	JWT_SECRET_KEY					= 'KoNaN'
	
	PROPAGATE_EXCEPTIONS			= True
	RESTX_MASK_SWAGGER 				= False
	
	API_TITLE 						= "Base Api"
	API_VERSION 					= "v1"
	
	CORS_HEADERS 					= 'Content-Type'
	CORS_RESOURCES    				= {r"/*": {"origins": "*"}}
	TESTING 						= True
	DEBUG 							= True
	FLASK_DEBUG 					= True
	FLASK_ENV 						= 'development' 	
	
	BASEDIR 						= os.path.abspath(os.path.dirname(__file__))
	MAX_CONTENT_LENGTH 				= 1000 * 1024 * 1024   # 1 * 1024 * 1024 = 1MB
	SQLALCHEMY_DATABASES_GEN		= os.path.join('db','database.db')
	SQLALCHEMY_DATABASE_URI 		= 'sqlite:///' + os.path.join(BASEDIR, SQLALCHEMY_DATABASES_GEN)
	SQLALCHEMY_TRACK_MODIFICATIONS 	= True
	SQLALCHEMY_ECHO 				= False
		
	LOGS  							= os.path.join(BASEDIR,'logs')
	DATA  							= os.path.join(BASEDIR,'data')
	# email 	
	EMAIL_ADDRESS  					= "konan72@gmail.com"
	

	

class ProductionConfig(object):
	"""
	Production configurations
	
	"""

	NAME 							= 'Base.app'
	JWT_SECRET_KEY					= 'KoNaN'
	
	PROPAGATE_EXCEPTIONS			= True
	RESTX_MASK_SWAGGER 				= False

	API_TITLE 						= "Base Api"
	API_VERSION 					= "v1"

	CORS_HEADERS 					= 'Content-Type'
	CORS_RESOURCES    				= {r"/*": {"origins": "*"}}

	TESTING 						= False
	DEBUG 							= False
	FLASK_DEBUG 					= True
	FLASK_ENV 						= 'production' 	
	
	BASEDIR 						= os.path.abspath(os.path.dirname(__file__))
	MAX_CONTENT_LENGTH 				= 1000 * 1024 * 1024
	SQLALCHEMY_DATABASES_GEN		= os.path.join('db','database.db')
	SQLALCHEMY_DATABASE_URI 		= 'sqlite:///' + os.path.join(BASEDIR, SQLALCHEMY_DATABASES_GEN)
	SQLALCHEMY_TRACK_MODIFICATIONS 	= False
	SQLALCHEMY_ECHO 				= False

	LOGS  							= os.path.join(BASEDIR,'logs')
	DATA  							= os.path.join(BASEDIR,'data')
	# email 	
	EMAIL_ADDRESS  					= "konan72@gmail.com"
	



app_config = {
	'development': DevelopmentConfig,
	'production' : ProductionConfig
}