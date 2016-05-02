# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Activity(models.Model):
    userid = models.ForeignKey('User', db_column='userId')  # Field name made lowercase.
    content = models.CharField(max_length=255)
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'activity'


class Collection(models.Model):
    exerciseid = models.ForeignKey('Exercise', db_column='exerciseId')  # Field name made lowercase.
    userid = models.ForeignKey('User', db_column='userId')  # Field name made lowercase.
    note = models.TextField(blank=True, null=True)
    righttime = models.IntegerField(db_column='rightTime', blank=True, null=True)  # Field name made lowercase.
    wrongtime = models.IntegerField(db_column='wrongTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'collection'


class Complaint(models.Model):
    userid = models.ForeignKey('User', db_column='userId', blank=True, null=True)  # Field name made lowercase.
    titleid = models.ForeignKey('Exercise', db_column='titleId', blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(blank=True, null=True)
    authorid = models.ForeignKey('User', db_column='authorid', blank=True, null=True)
    state = models.CharField(max_length=6, blank=True, null=True)
    topicid = models.ForeignKey('Topic', db_column='topicid', blank=True, null=True)
    opinionid = models.ForeignKey('Opinion', db_column='opinionid', blank=True, null=True)
    resourceid = models.ForeignKey('Source', db_column='resourceid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'complaint'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Exercise(models.Model):
    title = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)
    tips = models.CharField(max_length=255, blank=True, null=True)
    userid = models.ForeignKey('User', db_column='userId', blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(max_length=6, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    complaint = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'exercise'


class Opinion(models.Model):
    userid = models.ForeignKey('User', db_column='userId')  # Field name made lowercase.
    topicid = models.ForeignKey('Topic', db_column='topicId')  # Field name made lowercase.
    opinion = models.CharField(max_length=255)
    time = models.DateTimeField()
    state = models.CharField(max_length=6, blank=True, null=True)
    complaint = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'opinion'


class Source(models.Model):
    userid = models.ForeignKey('User', db_column='userId')  # Field name made lowercase.
    content = models.IntegerField()
    points = models.IntegerField()
    download = models.CharField(max_length=255)
    state = models.CharField(max_length=6, blank=True, null=True)
    complaint = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'source'


class Topic(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    time = models.DateTimeField()
    userid = models.ForeignKey('User', db_column='userID')  # Field name made lowercase.
    replytime = models.IntegerField(db_column='replyTime')  # Field name made lowercase.
    modifytime = models.DateTimeField(db_column='modifyTime')  # Field name made lowercase.
    complaint = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'topic'


class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    state = models.CharField(max_length=6, blank=True, null=True)
    points = models.IntegerField(blank=True, null=True)
    head = models.CharField(max_length=255, blank=True, null=True)
    flag = models.CharField(max_length=255, blank=True, null=True)
    complaint = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
