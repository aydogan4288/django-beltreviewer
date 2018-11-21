from django.db import models
import re
from datetime import datetime
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	def register_validator(self, postData):
		errors = {}

		if len(postData['username']) < 3:
			errors['username'] = "Username should be at least 3 characters."

		if len(postData['password']) < 8:
			errors['password'] = "Password should be at least 8 characters."
		elif postData['password'] != postData['confirm']:
			errors['password'] = "Password does not match."

		if len(postData['email']) < 1:
			errors['email'] = "Email cannot be blank."
		elif not EMAIL_REGEX.match(postData['email']):
			errors['email'] = "Not a valid email."
		elif User.objects.filter(email=postData['email']):
			errors['email'] = "Email is already taken."

		if not postData['dob']:
			errors['dob'] = "Date of birth field cannot be blank."
		elif postData['dob'] > str(datetime.now()):
			errors['dob'] = "Date of birth cannot be a future date."

		return errors

	def login_validator(self, postData):
		errors = {}

		if len(postData['passwordlogin']) < 1:
			errors['passwordlogin'] = "Password cannot be blank."

		if len(postData['emaillogin']) < 1:
			errors['emaillogin'] = "Email cannot be blank."
		elif not User.objects.filter(email=postData['emaillogin']):
			errors['emaillogin'] = "Email is not in database."

		else:
			user = User.objects.filter(email=postData['emaillogin'])
			print(user)
			if not bcrypt.checkpw(postData['passwordlogin'].encode(), user[0].password.encode()):
				errors['passwordlogin'] = "Passwords don't match"

		return errors

class MovieManager(models.Manager):
	def movie_validator(self, postData):
		errors = {}

		if len(postData['title']) < 2:
			errors['title'] = "Title must be greater than two characters"
		if not postData['year']:
			errors['year'] = "Year cannot be blank"
		elif int(postData['year']) > 2018:
			errors['year'] = "Year cannot be in the future"
		elif int(postData['year']) < 1888:
			errors['year'] = "Movies did not exist yet"
		return errors

class User(models.Model):
	username = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	dob = models.DateTimeField()
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	# favorited_movies (Many to many)
	# uploaded_movies (One to many)
	objects = UserManager()

class Movie(models.Model):
	title = models.CharField(max_length=255)
	year = models.IntegerField()
	favorited_users = models.ManyToManyField(User, related_name="favorited_movies")
	uploader = models.ForeignKey(User, related_name="uploaded_movies", on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = MovieManager()
