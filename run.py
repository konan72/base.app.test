import os, sys
from app import create_app


__author__      = 'KoNaN'

__version__     = '0.1.1.0'

app 			= create_app()


if __name__ == "__main__":
	app.run(host='127.0.0.1', threaded=True, debug=True, port=5000, use_reloader=True)