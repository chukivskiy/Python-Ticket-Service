# serializers.py
from rest_framework import serializers
from .models import Event, Ticket, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.password = validated_data.get('password', instance.password)
        instance.save()
        return instance


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('id', 'name', 'date', 'location', 'price')


    def create(self, validated_data):
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.date = validated_data.get('date', instance.date)
        instance.location = validated_data.get('location', instance.location)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'user', 'event', 'purchase_date')

    def create(self, validated_data):
        return Ticket.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.event = validated_data.get('event', instance.event)
        instance.purchase_date = validated_data.get('purchase_date', instance.purchase_date)

        instance.save()
        return instance