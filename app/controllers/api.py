import os
import re
import json
import requests
from dataclasses 		import dataclass
from datetime 			import datetime,timedelta
from flask 				import current_app as app
from app 				import db
from flask 				import jsonify, request, abort, make_response, render_template
from flask_restful 		import Resource, reqparse
from sqlalchemy 		import desc, asc, func, and_, or_
from flask_cors 		import cross_origin

from app.utils 			import customer_api_token_required, super_api_token_required, register_log_api





class cApi(Resource):
	
	@register_log_api(url="api", typ="GET")
	def get(self):
		try:
			data 				= { }
			date 				= '2024-05'
			url_crime_london 	= f"https://data.police.uk/api/stops-street?poly=51.5258338,-0.0206535:51.4621359,0.0057760:51.5177162,0.0895268:51.5258338,-0.0206535&date={date}"
			g 					= requests.get(url_crime_london)

			if g.status_code == 200:
				data = json.loads(g.text)

			response 							= make_response(jsonify(data), 200) 
			response.headers["Cache-Control"] 	= "no-cache, no-store, must-revalidate, public, max-age=0"
			response.headers["Pragma"] 			= "no-cache"
			response.headers["Expires"] 		= "0"
			return response

		except Exception as e:
			app.logger.error(f"cApi - Error - {e} - {datetime.now()}")
			raise e
		
			