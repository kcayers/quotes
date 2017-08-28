from __future__ import unicode_literals

from django.db import models

import datetime
import re, bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+._-]+@[a-zA-Z0-9+._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]\w+\ [a-zA-Z]\w+$')

class UserManager(models.Manager):
    def validate_registration(self, postData):
        errors = []

        if len(postData['name']) < 3:
            errors.append("Name should be longer than 3 letters")
        if len(postData['alias']) < 3:
            errors.append("Alias should be longer than 3 characters")
        if not NAME_REGEX.match(postData['name']):
            errors.append("Name should have a first and last name and letters only")
        if not EMAIL_REGEX.match(postData['email']):
            errors.append("Not a valid email")
        if len(postData['password']) < 8:
            errors.append("Password must be at least 8 characters")
        if postData['password'] != postData ['confirm']:
            errors.append("Password and Confirm must match")
        try:
            birth_date = datetime.datetime.strptime(postData['birth_date'], '%Y-%m-%d')
        except:
            errors.append("Birth Date may not be blank")
        try:
            User.objects.get(email=postData['email'])
            errors.append("Email already exits")
        except:
            pass
        today = datetime.datetime.today()
        if datetime.datetime.strptime(postData['birth_date'], "%Y-%m-%d") > today:
            errors.append("Birth date should be in the past")

        if len(errors):
            return errors
        encrypted = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(
            name = postData['name'],
            alias = postData['alias'],
            email = postData['email'],
            birth_date = postData['birth_date'],
            password = encrypted
            )
        return user.id

    def validate_login(self, postData):
        errors = []
        try:
            user = User.objects.get(user_name=postData['user_name'])
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                return user.id
            else:
                errors.append("wrong password")
        except:
            errors.append("invalid email")

        if len(errors):
            return errors

class QuoteManager(models.Manager):
    def validate_quote(self, postData, posted_id):
        errors = []
        if len(postData['quoted_by']) < 3:
            errors.append("Author name should be longer than 3 letters")
        if len(postData['quotation']) < 10:
            errors.append("Quotation should be longer than 10 letters")
        if len(errors):
            return errors

        quote = Quote.objects.create(
            quoted_by = postData['quoted_by'],
            quotation = postData['quotation'],
            posted_by = User.objects.get(id=posted_id),
            )
        return quote.id

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {} {} {}>".format(self.name, self.alias, self.email, self.birth_date)

class Quote(models.Model):
    quoted_by = models.CharField(max_length=255)
    quotation = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name = "posted_quotes")
    added_by = models.ManyToManyField(User, related_name = "added_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
    def __repr__(self):
        return "<Item object: {} {} {} {}>".format(self.quoted_by, self.quotation, self.posted_by.name, self.added_by.name)
