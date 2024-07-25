import re
import jwt

from functools 			import wraps
from flask 				import Flask, request, Response, jsonify
from flask 				import current_app as app
from datetime 			import datetime,timedelta
from sqlalchemy 		import func, and_, or_



def register_log_api(url, typ):
	def register_outer(fn):
		@wraps(fn)
		def register_inner(*args, **kwargs):
			if len(args) > 1:
				if args[1]:
					from ..models 			import LogApi
					_agent  	= request.headers.get('User-Agent')
					_ip     	= request.remote_addr 
					_logapi 	= LogApi(date=datetime.now(), url=url, typ=typ, ip=_ip, agent=_agent )			
					_logapi.save_to_db()	

			return fn(*args, **kwargs)
		return register_inner
	return register_outer


def check_auth(username, password):
	from app.models import Users	
	current_user = Users.query.filter_by(username=username).first()
	if current_user:
		return current_user.check_password(password), current_user
	return False, False
	

def required_auth(fn):	
	@wraps(fn)
	def decorated(self, *args, **kwargs):
		auth 		 = request.authorization
		remote_addr	 = request.remote_addr
		user 		 = None
		if not auth:
			app.logger.info(f"Users Upload - auth login failed - {remote_addr}  -  {datetime.now()}")
			return Response(
				'Could not verify your access level for that URL.\n'
				'You have to login with proper credentials', 401,
				{'WWW-Authenticate': 'Basic realm="Login Required"'}
			)
		else:
			check , user = check_auth(auth.username, auth.password)
			if not check:
				app.logger.info(f"Users Upload - auth login failed - {remote_addr} - {datetime.now()}")
				return Response(
					'Could not verify your access level for that URL.\n'
					'You have to login with proper credentials', 401,
					{'WWW-Authenticate': 'Basic realm="Login Required"'}
				)
		
		app.logger.info(f"Users Upload - access : {user.id} - {remote_addr} - {datetime.now()}")
		return fn(self, user, *args, **kwargs)
		
	return decorated


def super_api_token_required(fn):	
	@wraps(fn)
	def decorate(*args, **kwargs):
		remote_addr	 = request.remote_addr
		token = None
		if 'Authorization' in request.headers:
			token = request.headers.get('Authorization')
			
		if not token or token == 'null':
			app.logger.info(f"Token - Token is missing! - {remote_addr} - {datetime.now()}")
			return jsonify({'message': 'Token is missing!'})
		try:
			
			if jwt.get_unverified_header(token).get('alg') == 'HS256' and jwt.get_unverified_header(token).get('typ') == 'JWT':
			
				data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms='HS256', verify=False)
				
				if not data:
					app.logger.info(f"Token - Token is missing! - {remote_addr} - {datetime.now()}")
					return jsonify({'message': 'Token is not valid!'})

				if data.get('id'):
					from app.models import Users
					
					current_user = Users.query.filter_by(id=data.get('id')).first()		# add is_active

					if current_user:
						if token == current_user.token:				
							return (fn)(*args, **kwargs)
						else:
							app.logger.info(f"Token 1 - No Token found in the Database! - {remote_addr} - {datetime.now()}")
							return jsonify({'message': 'No Token found in the Database!'})	
					else:
						app.logger.info(f"Token 2 - No Token found in the Database! - {remote_addr} - {datetime.now()}")
						return jsonify({'message': 'No Token found in the Database!'})
				else:
					app.logger.info(f"Token 3 - No Token found in the Database! - {remote_addr} - {datetime.now()}")
					return jsonify({'message': 'No Token found in the Database!'})
			
		except jwt.DecodeError:	
			app.logger.error(f"Token - DecodeError Token is not valid! {datetime.now()}")
			return jsonify({'message': 'DecodeError Token is not valid!'})
		except jwt.ExpiredSignatureError:
			app.logger.error(f"Token - ExpiredSignatureError Token is expired! {datetime.now()}")
			return jsonify({'message': 'ExpiredSignatureError Token is expired!'})
		except Exception as e:
			app.logger.error(f"Token - Token is missing! {datetime.now()}")
			raise e
			return jsonify({'message': 'Token is missing!'})

	return decorate



def customer_api_token_required(fn):	
	@wraps(fn)
	def decorate(self):
		remote_addr	 = request.remote_addr
		token = None
		if 'Authorization' in request.headers:
			token = request.headers.get('Authorization')
			
		if not token or token == 'null':
			app.logger.info(f"Token Customer - Token is missing! - {remote_addr} - {datetime.now()}")
			return jsonify({'message': 'Token is missing!'})
		try:
			
			if jwt.get_unverified_header(token).get('alg') == 'HS256' and jwt.get_unverified_header(token).get('typ') == 'JWT':
			
				data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms='HS256', verify=False)
				
				if not data:
					app.logger.info(f"Token Customer - Token is missing! - {remote_addr} - {datetime.now()}")
					return jsonify({'message': 'Token is not valid!'})

				if data.get('code') and data.get('code_site'):					
					from app.models import Customers
					current_customer = Customers.query.filter(and_(Customers.code==data.get('code'),Customers.code_site==data.get('code_site'))).first() # add is_active
					
					if current_customer:
						if current_customer.is_active == True:
							if token == current_customer.token:	
								return (fn)(self, current_customer)
								#return fn(self, current_customer)
								#return (fn)(h, *args, **kwargs)							
							else:
								app.logger.info(f"Token 1 Customer- No Token found in the Database! - {remote_addr} - {datetime.now()}")
								return jsonify({'message': 'No Token found in the Database!'})	
						else:
							app.logger.info(f"Token 2 Customer- Customer is not active - {remote_addr} - {datetime.now()}")
							return jsonify({'message': 'Customer is not active'})	
					else:
						app.logger.info(f"Token 3 Customer- No Token found in the Database! - {remote_addr} - {datetime.now()}")
						return jsonify({'message': 'No Token found in the Database!'})
				else:
					app.logger.info(f"Token 4 Customer- No Token found in the Database! - {remote_addr} - {datetime.now()}")
					return jsonify({'message': 'No Token found in the Database!'})
			
		except jwt.DecodeError:	
			app.logger.error(f"Token Customer- DecodeError Token is not valid! {datetime.now()}")
			return jsonify({'message': 'DecodeError Token is not valid!'})
		except jwt.ExpiredSignatureError:
			app.logger.error(f"Token Customer- ExpiredSignatureError Token is expired! {datetime.now()}")
			return jsonify({'message': 'ExpiredSignatureError Token is expired!'})
		except Exception as e:
			app.logger.error(f"Token Customer - Token is missing! {datetime.now()}")
			raise e
			return jsonify({'message': 'Token is missing!'})

	return decorate