from app 				import api
from app.controllers  	import cHome 	as home_ns
from app.controllers  	import cApi 	as api_ns


# TABLE ROUTING
# HOME
api.add_resource(home_ns, "/")

# API
api.add_resource(api_ns, "/api")
