"""
KoNaN


# Commands 

# databases 
commands : flask db-init


# user
commands : flask create-super-user
commands : flask get-token-super-user


"""

 
import os
import click
import pick
import uuid
import datetime

from click 								import echo
from pick 								import pick

from sqlalchemy_utils 					import database_exists, create_database
from sqlalchemy 						import func, and_, or_


def register_commands(app, db):
	
	# command init db		
	@app.cli.command('db-init')
	def db_init():
		d = input("<< This operation will erase all data >> \nDo you want to continue the restore database ? (Y/n): ")
		
		if d == 'Y':
			if database_exists(app.config['SQLALCHEMY_DATABASE_URI']) == False: 
				create_database(app.config['SQLALCHEMY_DATABASE_URI'])
				print('Created database !')
		
			db.drop_all()
			db.create_all()
			click.echo('Initialized the SQLite database!')
		else:
			click.echo('Aborted operation!')


	# command create super user
	@app.cli.command('create-super-user')
	@click.option("--username", prompt='Insert your username', 	help="Insert username")
	@click.option("--name", 	prompt='Insert your name', 		help="Insert name")
	@click.option("--surname", 	prompt='Insert your surname', 	help="Insert surname")
	@click.option("--email", 	prompt='Insert your email', 	help="Insert email")
	@click.option("--password", prompt=True,	help="Insert password", hide_input=True, confirmation_prompt=True)
	def create_super_user(username, name, surname, email, password):
		from .models import Users		
		super_user = Users.query.filter(Users.username==username.strip(), Users.email == email.strip()).first()
		if not super_user:
			super_user = Users(username=username.strip(), name=name.strip(), surname=surname.strip(), email=email.strip(), password=password.strip())
			token = super_user.create_super_user()
			click.echo('Created Super User: {} - {} !'.format(username, email))
			click.echo('Token Super User:\n{}'.format(token))
		else:			
			click.echo('The already existing super user!')

	# command get super user token
	@app.cli.command('get-token-super-user')
	@click.option("--username", prompt='Insert your username', 	help="Insert username")
	@click.option("--email", 	prompt='Insert your email', 	help="Insert email")
	def get_token_super_user(username, email):
		from .models import Users		
		super_user = Users.query.filter(Users.username==username.strip(), Users.email == email.strip()).first()

		if super_user:
			click.echo('Token Super User: {} - {} \n{}'.format(super_user.username, super_user.email, super_user.token))
		else:		
			click.echo('The already existing super user!')

	