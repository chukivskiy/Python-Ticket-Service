from django.contrib import admin
from .models import Ticket, Event

admin.site.register(Ticket)

class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1

class EventAdmin(admin.ModelAdmin):
    inlines = [TicketInline]

admin.site.register(Event, EventAdmin)
