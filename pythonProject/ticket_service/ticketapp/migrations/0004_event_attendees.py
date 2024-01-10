# Generated by Django 4.2.7 on 2023-12-06 07:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ticketapp', '0003_remove_ticket_price_event_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(related_name='events_attending', through='ticketapp.Ticket', to=settings.AUTH_USER_MODEL),
        ),
    ]
