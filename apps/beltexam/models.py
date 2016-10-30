from __future__ import unicode_literals
from django.db import models
import bcrypt, re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def create_user(self, **kwargs):
        error_list = []
        if not kwargs['first_name'].isalpha():
            error_list.append('First Name is required and must contain only letters')
        if not kwargs['last_name'].isalpha():
            error_list.append('Last Name is required and must contain only letters')
        if not kwargs['email']:
            error_list.append('Email is required')
        if not email_regex.match(kwargs['email']):
            error_list.append('Email must be valid')
        if len(kwargs['password']) < 8:
            error_list.append('Password must contain at least 8 letters')
        if not kwargs['password'] == kwargs['c_password']:
            error_list.append('Password fields must match')
        if len(error_list) is 0:
            pw_hash = bcrypt.hashpw(kwargs['password'].encode(),bcrypt.gensalt())
            user = User.objects.create(first_name=kwargs["first_name"], last_name=kwargs['last_name'], email=kwargs['email'], password=pw_hash)
            return (True, user)
        else:
            return (False, error_list)

    def login(self, **kwargs):
        email = kwargs['email']
        pw = kwargs['password']
        error_list = []
        if not kwargs['email']:
            error_list.append('Email is required')
        if not email_regex.match(kwargs['email']):
            error_list.append('Email must be valid')
        if not kwargs['password']:
            error_list.append('Password is required')
        try:
            user = User.objects.get(email=email)
            input_pw = pw.encode()
            hashed_pw = user.password.encode()
            if bcrypt.hashpw(input_pw, hashed_pw) == hashed_pw:
                return(True, user)
            error_list.append('Email and Password do not match')
            return (False, error_list)
        except:
            error_list.append('Email and Password do not match')
        return (False, error_list)

    def update_user(self, **kwargs):
        print ("Update User")
        error_list = []
        if not kwargs['first_name'].isalpha():
            error_list.append('First Name is required and must contain only letters')
        if not kwargs['last_name'].isalpha():
            error_list.append('Last Name is required and must contain only letters')
        if not kwargs['email']:
            error_list.append('Email is required')
        if not email_regex.match(kwargs['email']):
            error_list.append('Email must be valid')
        if len(error_list) is 0:
            print ("No Errors")
            user = User.objects.filter(id=kwargs['id']).update(first_name=kwargs["first_name"], last_name=kwargs['last_name'], email=kwargs['email'])
            print user
            return (True, user)
        else:
            return (False, error_list)

    def update_password(self, **kwargs):
        error_list = []
        if len(kwargs['password']) < 8:
            error_list.append('Password must contain at least 8 letters')
        if not kwargs['password'] == kwargs['c_password']:
            error_list.append('Password fields must match')
        print error_list
        if len(error_list) is 0:
            print('no errors')
            pw_hash = bcrypt.hashpw(kwargs['password'].encode(),bcrypt.gensalt())
            user = User.objects.filter(id=kwargs['id']).update(password=pw_hash)
            return (True, user)
        else:
            return (False, error_list)

class MessageManager(models.Manager):
    def create_message(self, **kwargs):
        error_list = []
        if not kwargs['message']:
            error_list.append('Message is required')
        if len(error_list) is 0:
            message = Message.objects.create(message=kwargs["message"], user_id=kwargs["user_id"], sender_id=kwargs['sender_id'])
            return (True, message)
        else:
            return (False, error_list)

class CommentManager(models.Manager):
    def create_comment(self, **kwargs):
        error_list = []
        if not kwargs['comment']:
            error_list.append('Comment is required')
        if len(error_list) is 0:
            comment = Comment.objects.create(comment=kwargs["comment"], user_id=kwargs["user_id"], message_id=kwargs['message_id'])
            return (True, comment)
        else:
            return (False, error_list)

class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    user_id = models.ForeignKey(User)
    sender_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class Comment(models.Model):
    comment = models.TextField()
    user_id = models.ForeignKey(User)
    message_id = models.ForeignKey(Message)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()
