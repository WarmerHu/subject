# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class Activity(models.Model):
    id = models.IntegerField(primary_key=True)
    userid = models.ForeignKey('User', db_column='userId') # Field name made lowercase.
    content = models.CharField(max_length=255)
    time = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'activity'

class Collection(models.Model):
    id = models.IntegerField(primary_key=True)
    exerciseid = models.ForeignKey('Exercise', db_column='exerciseId') # Field name made lowercase.
    userid = models.ForeignKey('User', db_column='userId') # Field name made lowercase.
    note = models.TextField(blank=True)
    righttime = models.IntegerField(db_column='rightTime', blank=True, null=True) # Field name made lowercase.
    wrongtime = models.IntegerField(db_column='wrongTime', blank=True, null=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'collection'

class Exercise(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    tips = models.CharField(max_length=255, blank=True)
    userid = models.ForeignKey('User', db_column='userId', blank=True, null=True) # Field name made lowercase.
    state = models.CharField(max_length=6, blank=True)
    class Meta:
        managed = False
        db_table = 'exercise'

class Opinion(models.Model):
    id = models.IntegerField(primary_key=True)
    userid = models.ForeignKey('User', db_column='userId') # Field name made lowercase.
    topicid = models.ForeignKey('Topic', db_column='topicId') # Field name made lowercase.
    opinion = models.CharField(max_length=255)
    time = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'opinion'

class Source(models.Model):
    id = models.IntegerField(primary_key=True)
    userid = models.ForeignKey('User', db_column='userId') # Field name made lowercase.
    content = models.IntegerField()
    points = models.IntegerField()
    download = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'source'

class Topic(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    content = models.TextField()
    time = models.DateTimeField()
    userid = models.ForeignKey('User', db_column='userID') # Field name made lowercase.
    replytime = models.IntegerField(db_column='replyTime') # Field name made lowercase.
    modifytime = models.DateTimeField(db_column='modifyTime') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'topic'

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    state = models.CharField(max_length=6, blank=True)
    points = models.IntegerField(blank=True, null=True)
    head = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = False
        db_table = 'user'

