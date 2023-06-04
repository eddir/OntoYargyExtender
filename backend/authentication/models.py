from django.db import models

class Request(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, default=None)
    organization = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    goal = models.CharField(max_length=255, blank=True, null=True)