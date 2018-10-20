# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..login.models import User
from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

# class Quotes(models.Model):
#     quote = models.CharField(max_length=255)
#     author = models.ForeignKey(Author, related_name="quotes")
#     poster = models.ForeignKey(User, related_name="poster")
#     def __str__(self):
#         return self.quote

class QuoteManager(models.Manager):
    def validate_quote(self, post_data):
        errors = []

        if len(post_data['author']) < 1 or len(post_data['quote']) < 1:
            errors.append('Please fill out all fields.')
        if not "author" in post_data and len(post_data['author']) < 3:
            errors.append('Entered names must exceed 3 characters in length.')

        if len(post_data['quote']) < 10 :
            errors.append('Please enter 10 or more characters in the quote section.')
        return errors

    def create_quote(self, clean_data, user_id):
        author = Author.objects.create(name=clean_data['author'])
        quote = Quote.objects.create(
                quote=clean_data['quote'], author=author)
        return self.create(
            quote = clean_data['quote'],
            author = clean_data['author'],
            poster = User.objects.get(id=user_id)
        )

    def recent_quotes(self):
        return (self.all().order_by('-created_at')[:3], self.all().order_by('-created_at')[3:])

class Quote(models.Model):
    quote = models.CharField(max_length=255)
    poster = models.ForeignKey(User, related_name="quote_creator")
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
    def __str__(self):
        return "Quote: {}".format(self.quote)

class Favorite(models.Model):
    quote = models.ForeignKey(Quote, related_name="fave_quotes")
    poster = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __str__(self):
        return self    