from __future__ import annotations
from django.db import models
from autoslug import AutoSlugField
from django.urls import reverse

# Create your models here.

class Club(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    description = models.TextField()
    members = models.ManyToManyField('auth.User', through='Membership', related_name='memberships')
    slug = AutoSlugField(unique_with='id', populate_from='name')
    
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"slug": self.slug})
    
    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, default='pending')
    
    def approve(self):
        self.role = 'member'
    
    def __str__(self):
        return self.user.username + ' is ' + self.role + ' of ' + self.club.name
    
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    def __str__(self):
        return self.name