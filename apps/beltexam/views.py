from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import User, Friendships


def index(request):
    return render(request, 'beltexam/index.html')

def users_register(request):
    if request.method == "POST":
        result = User.objects.create_user(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'], c_password=request.POST['c_password'])
        if result[0]:
            request.session['first_name'] = result[1].first_name
            request.session['email'] = result[1].email
            request.session['id'] = result[1].id
            id = result[1].id
            return redirect(reverse('users_manage'))
        else:
            messages.add_message(request, messages.INFO, result[1])
            return redirect(reverse('index'))

def login(request):
    if request.method == "POST":
        result = User.objects.login(email=request.POST['email'], password=request.POST['password'])
        if result[0]:
            request.session['first_name'] = result[1].first_name
            request.session['email'] = result[1].email
            request.session['id'] = result[1].id
            return redirect(reverse('users_manage'))
        else:
            messages.add_message(request, messages.INFO, result[1])
            return redirect(reverse('index'))

def users_logout(request):
    request.session.clear()
    return redirect(reverse('index'))


def users_manage(request):

    friends = Friendships.objects.filter(user__id=request.session['id'])
    users = User.objects.all()
    context = {
            'users' : User.objects.exclude(id = request.session['id']),
            'friends' : friends
            }
    return render(request, 'beltexam/users_manage.html', context)

def show_user(request, id):
    context = {
        'user' : User.objects.get(id=id)
    }
    return render(request, 'beltexam/show.html', context)


def users_delete(request, id):
    if request.method == 'POST':
        users = User.objects.all()
        if len(users) < 2:
            User.objects.get(id=id).delete()
            return redirect(reverse('logout'))
        else:
            User.objects.get(id=id).delete()
            return redirect(reverse('users_manage'))

def add_friend(request, id):
    user = User.objects.get(id=id)
    logged_user = User.objects.get(id=request.session['id'])
    result = Friendships.objects.create(user=logged_user, friend=user)
    return redirect(reverse('users_manage'))
