# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# from django.db import models
import random, string
from django.db.models import IntegerField, Model, CharField, ForeignKey, CASCADE, TextField, BooleanField
from django_mysql.models import ListTextField

class TTP(Model):
    Tactic = CharField(max_length=100,null=True)
    # Technique = TextField(max_length=400,null=True)
    Technique = ListTextField(base_field=CharField(max_length=200),size=200,null=True)
    TotalTech = IntegerField(blank=True, null=True)
    FuncTact = CharField(max_length=100,null=True)

    def __str__(self):
        return self.Tactic

class Tactic(Model):
    tacticName = CharField(max_length=100,null=True)

    def __str__(self):
        return self.tacticName

class Techniques(Model):
    techniqueName = CharField(max_length=100,null=True)
    tactic = ForeignKey(TTP, on_delete=CASCADE, default='', null=True)
    techniqueId = CharField(max_length=100,null=True)
    techniqueRepeat = IntegerField(blank=True, default=1)
    SubTechnique = BooleanField(default=False)
    techColor = CharField(max_length=100,null=True)

    def __str__(self):
        return self.techniqueName

    # class Meta:
    # ordering = ['headline']
    # Name = CharField(max_length=100)

'''
class Contact(Model):
    name = CharField(max_length=100)
    email = CharField(max_length=100,null=True)
    message = CharField(max_length=100,null=True)

    def __str__(self):
        return self.name

'''