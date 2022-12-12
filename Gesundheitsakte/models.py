from django.db import models

class Document(models.Model):
    name = models.CharField(max_length=30)
    path = models.FileField()
    owner = models.ForeignKey('auth.User',on_delete=models.CASCADE)
    shared = models.ManyToManyField('share')

class share(models.Model):
    username = models.CharField(max_length=30)
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE)
