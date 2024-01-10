from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    attendees = models.ManyToManyField(User, through='Ticket')
    def __str__(self):
        return self.name



class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
    purchase_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} - {self.event.name}"



