from django.db import models

class Document(models.Model):
    id = models.IntegerField(primary_key=True,unique=True,editable=False)
    name = models.CharField(max_length=30)
    path = models.FileField()
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    shared = models.ManyToManyField('share')

class share(models.Model):
    #user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    share_id = models.IntegerField(primary_key=True, unique=True, editable=False)
    id = models.IntegerField(editable=False)
    username = models.CharField(max_length=50,default="")
