import sys, os
from flask import Flask, request, redirect, render_template, abort, session, flash

import default_config
from database_handler import *
import user_handler

if not default_config.USEDUMMYDATABASE:
	import SQL_handler
else:
	import dummy_database as SQL_handler

def create_app():
	app = Flask(__name__, instance_relative_config=True)
	app.secret_key = os.urandom(24)


	@app.route('/')
	def home():

		products = []
		productIds = SQL_handler.getAllProductId()
		for productId in productIds:
			products.append(SQL_handler.getProductFromDatabase(productId))

		return render_template('home.html', args={'categories': SQL_handler.getCategories(), 'user': user_handler.get_user()})


	@app.route('/product/<id>')
	def product(id):
		try:
			product = SQL_handler.getProductFromDatabase(id)
			return render_template('product.html', args={'product': product, 'user': user_handler.get_user()})

		except database_handler.NotInDatabase:
			abort(404)


	@app.route('/category/<id>')
	def category(id):

		return render_template('categories.html', args={'products': SQL_handler.getProductsByCategoryFromDatabase(id), 'user': user_handler.get_user()})
		

	@app.route('/login', methods = ['GET', 'POST'])
	def login():

		if request.method == 'POST':
			if user_handler.login_parse(request.form['username'], request.form['password']):
				flash('Welcome %s' % user_handler.get_user().alias)
				return redirect('/')

			else:
				flash('Invalid username or password')

		return render_template('login.html', args={'user': user_handler.get_user()})


	@app.route('/logout')
	def logout():
		if user_handler.get_user() is None:	
			abort(404)

		user_handler.logout_parse()
		flash("You've been logged out")
		return redirect('/')


	@app.route('/signup', methods = ['GET', 'POST'])
	def signup():

		if request.method == 'POST':
			if user_handler.signup_parse(request.form['username'], request.form['password']):
				user_handler.login_parse(request.form['username'], request.form['password'])
				flash('Welcome %s' % user_handler.get_user().alias)
				return redirect('/')

			else:
				flash('Invalid username or password')

		return render_template('login.html', args={'user': user_handler.get_user()})


	@app.route('/manager', methods = ['GET',])
	def manager():
		if user_handler.get_user() is None or user_handler.get_user().clearance > 1:	
			abort(404)

		return render_template('manager.html', args={'users': SQL_handler.getAllUsers(), 'user': user_handler.get_user(), 'products': SQL_handler.getAllProducts()})


	@app.route('/manageUser/<id>', methods = ['GET', 'POST'])
	def manageUser(id):
		if user_handler.get_user() is None or user_handler.get_user().clearance > 1:	
			abort(404)

		userToManage = SQL_handler.getUserById(id)

		if request.method == 'POST':

			userToManage.alias = request.form['alias']

			if user_handler.get_user().clearance == 0:
				userToManage.clearance = request.form['clearance']
	
			if request.form['password'] != "":
				user_handler.update_password(userToManage, request.form['password'])
			
			SQL_handler.update_user(userToManage)

		return render_template('manageUser.html', args={'users': SQL_handler.getAllUsers(), 'user': user_handler.get_user(), 'userToManage': userToManage})


	@app.route('/manageProduct/<id>', methods = ['GET', 'POST'])
	def manageProduct(id):
		productToManage = SQL_handler.getProductFromDatabase(id)

		if user_handler.get_user() is None or user_handler.get_user().clearance > 1 or SQL_handler.getProductFromDatabase(id) is None:	
			abort(404)

		if request.method == 'POST':
			productToManage.name = request.form['name']
			productToManage.price = request.form['price']
			productToManage.description = request.form['description']
			productToManage.category = request.form['category']

			SQL_handler.updateProductIntoDatabase(productToManage)
			

		return render_template('manageProduct.html', args={'users': SQL_handler.getAllUsers(), 'categories': SQL_handler.getCategories(), 'user': user_handler.get_user(), 'productToManage': productToManage})


	return app
	

if __name__ == "__main__":

    app = create_app()
    app.run(host='0.0.0.0', debug=default_config.DEBUG)
