import os
from flask import render_template, url_for, flash,redirect, request
from flaskblog2 import app, db, bcrypt
from flaskblog2.forms import RegistrationForm, LoginForm,UpdateAccountForm,PostForm
from flaskblog2.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required




@app.route('/')
@app.route('/home')
def home():
	posts = Post.query.all()
	return render_template('home.html', posts=posts, title='Home  page',home_title='Welcome to home tours', content='Welcome to our site get the experience that you have never had')


@app.route('/about')
def about():
	return render_template('about.html', title='About page',home_title='Welcome to About page', content='Welcome to our learn about us')

@app.route('/register', methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('home'))
	form = RegistrationForm()
	if form.validate_on_submit():
		pw_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		user = User(username=form.username.data, email=form.email.data, password=pw_hash)
		db.session.add(user)
		db.session.commit()
		flash("Account created suceessful.You can now login",'success')
		return redirect(url_for('login'))
	return render_template('register.html', title='Registration page', form=form,home_title='Welcome !!Register here', content='Create an account and have an exclusive experience')

@app.route('/login', methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('home')) 
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			flash('You have been logged in', 'success')
			return redirect(url_for('home'))
		else:
			flash('login not successful. PLease check username and password', 'danger')
			return redirect(url_for('login'))
	return render_template('login.html', title='Login page', form=form,home_title='Welcome !!Login here', content='Get to learn many of the packages that we offer')


@app.route('/logout')
def logout():
	logout_user()
	flash('Logout successful ', 'success')
	return redirect(url_for('home'))

def save_picture(form_picture):
	_,f_ext = os.path.splitext(form_picture.filename)
	pic_name = _ + f_ext
	print(pic_name)
	picture_path = os.path.join(app.root_path  + "/static/images/profile_imgs", pic_name)
	form_picture.save(picture_path)
	return pic_name

	

@app.route('/account', methods=['GET','POST'])
def account():
	form = UpdateAccountForm()
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash("Update account successful", 'success')
		return redirect(url_for('account'))
	form.username.data = current_user.username
	form.email.data = current_user.email

	image_file = url_for('static', filename='images/profile_imgs/'+ current_user.image_file) 
	print(current_user.image_file)
	return render_template('account.html', title='Account', image_file=image_file, form=form,home_title='As the admin what do have to offer', content='Make a good profile and market well')

def save_post_img(form_picture):
	_,f_ext = os.path.splitext(form_picture.filename)
	pic_name = _ + f_ext
	picture_path = os.path.join(app.root_path  + "/static/images/post_imgs", pic_name)
	form_picture.save(picture_path)
	return pic_name

@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		if form.post_image.data:
			picture = form.post_image.data
			_,f_ext = os.path.splitext(picture.filename)
			pic_name = _ + f_ext
			picture_path = os.path.join(app.root_path  + "/static/images/post_imgs", pic_name)
			picture.save(picture_path)
			
			path = url_for('static', filename='images/post_imgs/' + pic_name ) 
			post = Post(title = form.title.data,content=form.content.data,post_image = path, author=current_user)
			db.session.add(post)
			db.session.commit()
			flash('Addition successful', 'success')
			return redirect(url_for('home'))
		else:
			post = Post(title = form.title.data,content=form.content.data, author=current_user)
			db.session.add(post)
			db.session.commit()
			flash('Addition successful', 'success')
			return redirect(url_for('home'))

	image_file = url_for('static', filename='images/profile_imgs/'+ current_user.image_file) 	
	return render_template('create_post.html', form=form, title="New post",home_title='Add content', content='Advertise the latest packages')


@app.route('/post/detail/<int:post_id>', methods=['GET','POST'])
def post_detail(post_id):
	post = Post.query.filter_by(id=post_id).first()
	form = PostForm()

	if form.validate_on_submit():
		if form.post_image.data:
			picture_file = form.post_image.data
			_, f_ext = os.path.splitext(picture_file.filename)
			pic_name = _+f_ext
			picture_path = os.path.join(app.root_path  + "/static/images/post_imgs", pic_name)
			picture_file.save(picture_path)
			path = url_for('static', filename='images/post_imgs/' + pic_name ) 
			post.post_image = path
			print(path)


		post.title = form.title.data
		post.content = form.content.data

		db.session.add(post)
		db.session.commit()
		flash('Update successful', 'success')
		return redirect(url_for('post_detail', post_id=post.id))
	else:
		form.title.data = post.title
		form.content.data = post.content
		image_file = post.post_image
		_,f_ext = os.path.splitext(image_file)
		pic_path= _ +f_ext
		
		
	
		return render_template('post_detail.html',post=post, title="Detail page",form=form,home_title=post.title, content='Get to learn many of the packages that we offer')



@app.route('/post/delete/<int:post_id>')
def delete_post(post_id):
	post = Post.query.filter_by(id=post_id).first()
	db.session.delete(post)
	db.session.commit()

	flash("Delete suceessful", 'success')
	return redirect(url_for('home'))
	