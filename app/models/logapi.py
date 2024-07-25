from flask 						import current_app as app
from app 						import db
from datetime 					import datetime, timedelta
from sqlalchemy 				import Column, Integer, String, Boolean, ForeignKey, Text, DateTime, ForeignKeyConstraint
from sqlalchemy 				import func, and_, or_
from sqlalchemy.orm 			import relationship





class LogApi(db.Model):
	
	__tablename__ 	= 'logapi'

	id 				= Column(Integer, primary_key=True, autoincrement=True, nullable=False)		
	date 			= Column(DateTime(timezone=True), nullable=False)
	url 			= Column(Text, nullable=False)
	typ 			= Column(String(15), nullable=False)
	ip 				= Column(String(15), nullable=False)
	agent 			= Column(Text, nullable=False)


	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()


	def __repr__(self):
		return '<Log> {} {}>'.format(self.id, self.user_id)