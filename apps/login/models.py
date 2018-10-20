# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt
from django.db import models

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[A-Za-z]\w+$')

class UserManager(models.Manager):
    def validate_login(self, post_data):
        errors = []
        if len(self.filter(email=post_data['email'])) > 0:
            user = self.filter(email=post_data['email'])[0]
            if not bcrypt.checkpw(post_data['password'].encode(), user.password.encode()):
                errors.append('Email/password is incorrect.')
        else:
            errors.append('Email/password is incorrect.')

        if errors:
            return errors
        return user

    def validate_registration(self, post_data):
        errors = []
        if len(post_data['name']) < 2 or len(post_data['alias']) < 2:
            errors.append("Name must include at least 3 characters.")
        if len(post_data['password']) < 8:
            errors.append("Your password must include at least 8 characters.")            
        if not re.match(NAME_REGEX, post_data['name']):
            errors.append('Your name can only consist of letters.')
        if not re.match(EMAIL_REGEX, post_data['email']):
            errors.append("Invalid email format.")
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors.append("Email is already registered.")
        if post_data['password'] != post_data['password_confirm']:
            errors.append("Your passwords do not match.")

        if not errors:
            hashed = bcrypt.hashpw((post_data['password'].encode()), bcrypt.gensalt(5))
            new_user = self.create(
                name=post_data['name'],
                alias=post_data['alias'],
                email=post_data['email'],
                bday=post_data['bday'],
                password=hashed
            )
            return new_user
        return errors


class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    bday = models.DateField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __str__(self):
        return self.email