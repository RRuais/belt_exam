from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import User, Message, Comment


def index(request):
    return render(request, 'beltexam/index.html')

def signin(request):
    return render(request, 'beltexam/signin.html')

def register(request):
    return render(request, 'beltexam/register.html')

def users_register(request):
    if request.method == "POST":
        result = User.objects.create_user(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=request.POST['password'], c_password=request.POST['c_password'])
        if result[0]:
            request.session['first_name'] = result[1].first_name
            request.session['email'] = result[1].email
            request.session['id'] = result[1].id
            id = result[1].id
            return redirect('wall', id)
        else:
            messages.add_message(request, messages.INFO, result[1])
            return redirect(reverse('register'))

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
            return redirect(reverse('signin'))

def users_logout(request):
    request.session.clear()
    return redirect(reverse('index'))


def users_manage(request):
    context = {
        'users' : User.objects.all()
    }
    return render(request, 'beltexam/users_manage.html', context)

def users_edit(request, id):
    context = {
        'user' : User.objects.get(id=id)
    }
    return render(request, 'beltexam/users_edit.html', context)

def users_delete(request, id):
    if request.method == 'POST':
        users = User.objects.all()
        if len(users) < 2:
            User.objects.get(id=id).delete()
            return redirect(reverse('logout'))
        else:
            User.objects.get(id=id).delete()
            return redirect(reverse('users_manage'))

def users_update(request, id):
    if request.method == "POST":
        result = User.objects.update_user(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], id=id)
        if result[0]:
            user = User.objects.get(id=id)
            request.session['first_name'] = user.first_name
            request.session['email'] = user.email
            return redirect(reverse('users_manage'))
        else:
            messages.add_message(request, messages.INFO, result[1])
            return redirect(reverse('users_edit'))

def update_password(request, id):
    if request.method == "POST":
        result = User.objects.update_password(password=request.POST['password'], c_password=request.POST['c_password'], id=id)
        if result[0]:
            return redirect(reverse('users_manage'))
        else:
            messages.add_message(request, messages.INFO, result[1])
            return redirect('edit', id)

def users_wall(request, id):
    user = User.objects.get(id=id)
    messages = Message.objects.filter(user_id=user)
    for mess in messages:
        sender = User.objects.get(id=mess.sender_id)
        mess.sender_id = sender.first_name

    comments = Comment.objects.all()

    context = {
        'user' : user,
        'messages' : messages,
        'comments' : comments

    }


    return render(request, 'beltexam/wall.html', context)

def post_messages(request, id):
    user = User.objects.get(id=id)
    # logged_user = User.objects.get(id=request.session['id'])
    result = Message.objects.create_message(message=request.POST['message'], user_id=user, sender_id=request.session['id'])
    if result[0]:
        return redirect('wall', id)
    else:
        messages.add_message(request, messages.INFO, result[1])
        return redirect('edit', id)
    return redirect('wall', id)


def delete_messages(request, id):
    message = Message.objects.get(id=id)
    user = message.user_id
    user_id = user.id
    Message.objects.get(id=id).delete()

    return redirect('wall', user_id)

def post_comment(request, id, user):
    user_id = User.objects.get(id=request.session['id'])
    message_id = Message.objects.get(id=id)
    result = Comment.objects.create_comment(comment=request.POST['comment'], user_id=user_id, message_id=message_id)
    if result[0]:
        return redirect('wall', user)
    else:
        messages.add_message(request, messages.INFO, result[1])
        return redirect('wall', user)

def delete_comment(reguest, id, user):
    Comment.objects.get(id=id).delete()
    return redirect('wall', user)
