
import os
import jwt

from flask 					import current_app as app
from app 					import db
from uuid 					import uuid4
from sqlalchemy 			import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm 		import relationship, backref
from werkzeug.security 		import generate_password_hash, check_password_hash
from datetime 				import datetime, timedelta


class Users(db.Model):
	
	__tablename__ = 'users'

	id          	= Column(String(255), 	nullable=False, unique=True, primary_key=True)
	email           = Column(String(300), 	nullable=False, unique=True)
	username        = Column(String(300), 	nullable=False, unique=True)
	name           	= Column(String(300), 	nullable=False, unique=False)
	surname         = Column(String(300), 	nullable=False, unique=False)	
	password        = Column(String(300), 	nullable=False, unique=False)	
	created_at      = Column(DateTime(timezone=True), nullable=False, default=datetime.now(), unique=False)
	is_active       = Column(Boolean(), 	default=True, 	nullable=False, unique=False)	
	language 		= Column(String(255), 	nullable=False, unique=False, default='it')
	token 			= Column(String(300), 	nullable=False, unique=False)	
	

	@classmethod
	def generate_uuid(self):
		return str(uuid4())

	@classmethod
	def generate_password(self, value):
		return generate_password_hash(value, method='scrypt')
		
	def create_super_user(self):
		try:
			self.id 		= self.generate_uuid()
			self.password 	= self.generate_password(self.password)
	
			payload = {				
				'id' 		: self.id,
				'username' 	: self.username,
				'email' 	: self.email
			}	
			
			self.token = jwt.encode(payload,  app.config['JWT_SECRET_KEY'], algorithm='HS256')
			
			db.session.add(self)
			db.session.commit()

			return self.token			

		except Exception as e:
			app.logger.error(f"Users class - Error in create_super_user : {e}")
			raise e
	
	def check_password(self, password):
		if check_password_hash(self.password, password):
			return True
		else:
			return False

	def __repr__(self):
		return "<User :{0} {1} >".format(self.id, self.email)    
