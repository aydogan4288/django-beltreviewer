from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from .models import User, Movie
import bcrypt


def index(request):
	if 'user_id' in request.session:
		return redirect('/dash')
	else:
		context = {
			"users": User.objects.all(),
		}
		return render(request, "myapp/index.html", context)

def register(request):
	errors = User.objects.register_validator(request.POST)

	if len(errors):
		for key, error in errors.items():
			messages.add_message(request, messages.ERROR, error, extra_tags='register')
		return redirect('/')
	else:
		pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		user = User.objects.create(username=request.POST["username"], email=request.POST["email"], dob=request.POST["dob"], password=pwhash.decode('utf-8'))
		request.session["user_id"] = user.id
		return redirect('/dash')

def login(request):
	errors = User.objects.login_validator(request.POST)
	print(errors)
	if len(errors):
		for key, error in errors.items():
			messages.add_message(request, messages.ERROR, error, extra_tags='login')
		return redirect('/')

	else:
		user = User.objects.get(email=request.POST['emaillogin'])
		request.session['user_id'] = user.id
		print('session id is', request.session['user_id'])
		return redirect('/dash')

def dash(request):
	if 'user_id' not in request.session:
		return redirect('/')
	else:
		other_movies = []
		all_movies = Movie.objects.all()
		mymovies = User.objects.get(id=request.session['user_id']).favorited_movies.all()
		for movie in all_movies:
			if movie not in mymovies:
				other_movies.append(movie)

		context = {
			"movies": other_movies,
			"user" : User.objects.get(id= request.session['user_id']),
			"mymovies": mymovies,
		}
		return render(request, "myapp/dash.html", context)



def new(request):
	
	return render(request, "myapp/new.html")

def create(request):
	errors = Movie.objects.movie_validator(request.POST)
	if errors:
		for key, error in errors.items():
			messages.add_message(request, messages.ERROR, error)
		print(errors)
		return redirect('/new')
	else:
		movie = Movie.objects.create(title=request.POST["title"], year=request.POST["year"], uploader_id = request.session['user_id'])
		movie.favorited_users.add(User.objects.get(id=request.session['user_id']))
		#this is creating the joined 
		return redirect('/dash')

def clear(request):
	request.session.clear()
	return redirect("/")

def favorite(request, movieid):
	movie = Movie.objects.get(id=movieid)
	movie.favorited_users.add(User.objects.get(id=request.session['user_id']))
	return redirect('/dash')


def unfavorite(request, movieid):
	movie = Movie.objects.get(id=movieid)
	movie.favorited_users.remove(User.objects.get(id=request.session['user_id']))
	return redirect('/dash')


def delete(request, movieid):
	Movie.objects.get(id=movieid).delete()
	return redirect('/dash')


def show(request, movieid):
	movie = Movie.objects.get(id=movieid)
	context = {
		"movie": movie,
		"users": movie.favorited_users.all(),
	}
	return render(request, 'myapp/show.html', context)







