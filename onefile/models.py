from django.db import models

# Create your models here.
import json


class Users(models.Model):
    '''用户数据，用于登陆验证'''
    @classmethod
    def createUser(cls, account, password, name):
        user = cls(uaccount=account, upassword=password,
                   uname=name, ufiles=json.dumps([]))
        return user
    uaccount = models.CharField(max_length=100)
    upassword = models.CharField(max_length=30)
    uname = models.CharField(max_length=100)
    ufiles = models.CharField(max_length=1024,default='[]')

    class Meta:
        db_table = "Users"


class Files(models.Model):
    @classmethod
    def createFile(cls, filename, filesize, filepath, belong):
        file = cls(filename=filename, filesize=filesize,
                   filepath=filepath, belong=belong)
        return file
    filename = models.CharField(max_length=255)
    filesize = models.CharField(max_length=255)
    filepath = models.CharField(max_length=255)
    belong = models.CharField(max_length=255)

    class Meta:
        db_table = "Files"
