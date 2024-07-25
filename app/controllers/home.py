
from flask 				import current_app as app
from flask 				import jsonify, request, abort, make_response, render_template
from flask_restful 		import Resource, reqparse

#from app.models 		import Users, Roles, Permission
#from app.utils 		import api_token_required, register_log_api, api_token_supervisor_required




class cHome(Resource):
	
	@classmethod
	def get(self):
		try:
			
			app.logger.info("Open home")

			headers = {'Content-Type': 'text/html'}
			return make_response(render_template('index.html'), 200, headers)

		except Exception as e:
			return jsonify({"message": "{}".format(e) })
			raise e