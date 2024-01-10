from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime
from .models import User, Event, Ticket
from .serializers import UserSerializer, EventSerializer, TicketSerializer
from jinja2 import Template
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
#     def get(self, request):
#         queryset = User.objects.all()
#         return Response({'posts': UserSerializer(queryset, many=True).data})
# User views

# queryset = User.objects.all()
# return Response(UserSerializer(queryset, many=True).data)
class UserSetView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        user_list = User.objects.all()
        return render(request, 'user_list.html', {'user_list': user_list})

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserDetailView(generics.ListAPIView):
    @swagger_auto_schema(responses={200: UserSerializer()})
    def get(self, request, *args,  **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            # user_list = User.objects.all()
            # return render(request, 'user_list.html', {'user_list': user_list})
            return Response({"error": "Method GET is not allowed"})
        try:
            user = User.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exist"}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserSerializer(user).data)

    @swagger_auto_schema(request_body=UserSerializer, responses={200: UserSerializer()})
    def put(self, request, *args,  **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            user = User.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exist" }, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: "Object deleted successfully"})
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"ERROR": "Delete Method Is Not Allowed"})

        # deleting an object from api

        try:
            instance = User.objects.get(pk=pk)
            instance.delete()
        except:
            return Response({"ERROR": "Object Not Found !"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"post": f"Object {str(pk)} is deleted"})

# Event views
class EventSetView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        event_list = Event.objects.all()
        return render(request, 'event_list.html', {'event_list': event_list})

    @swagger_auto_schema(request_body=EventSerializer)
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(generics.ListAPIView):
    @swagger_auto_schema(responses={200: EventSerializer()})
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            # queryset = Event.objects.all()
            # return Response(EventSerializer(queryset, many=True).data)
            return Response({"error": "Method GET is not allowed"})
        else:
            try:
                event = Event.objects.get(pk=pk)
                return Response(EventSerializer(event).data)
            except:
                return Response({"error": "Object does not exist" }, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=EventSerializer, responses={200: EventSerializer()})
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            user = Event.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exist"})
        serializer = EventSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: "Object deleted successfully"})
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"ERROR": "Delete Method Is Not Allowed"})

        # deleting an object from api

        try:
            instance = Event.objects.get(pk=pk)
            instance.delete()
        except:
            return Response({"ERROR": "Object Not Found !"})

        return Response({"post": f"Object {str(pk)} is deleted"})


# Ticket views
class TicketSetView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        ticket_list = Ticket.objects.all()
        return render(request, 'ticket_list.html', {'ticket_list': ticket_list})

    @swagger_auto_schema(request_body=TicketSerializer)
    def post(self, request):
        event_id = request.data.get('event', None)
        user_id = request.data.get('user', None)
        user_exists = User.objects.filter(pk=user_id).exists()
        event_exists = Event.objects.filter(pk=event_id).exists()

        if not user_exists:
            return Response({"error": f"There is no user with {str(user_id)}"})
        if not event_exists:
            return Response({"error": f"There is no event with {str(event_id)}"})

        purchase_date_str = request.data.get("purchase_date", None)
        if purchase_date_str:
            purchase_date = datetime.strptime(purchase_date_str, "%Y-%m-%d").date()
        else:
            purchase_date = datetime.now().date()

        event = Event.objects.filter(pk=event_id).first()

        if purchase_date > event.date:
            return Response({"error": "Ticket purchase time has expired"})

        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketDetailView(generics.ListAPIView):

    @swagger_auto_schema(responses={200: TicketSerializer()})
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            if not pk:
                # ticket_list = Ticket.objects.all()
                # return render(request, 'ticket_list.html', {'ticket_list': ticket_list})
                return Response({"error": "Method GET is not allowed"})
        try:
            ticket = Ticket.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exist" }, status=status.HTTP_404_NOT_FOUND)

        return Response(TicketSerializer(ticket).data)

    @swagger_auto_schema(request_body=TicketSerializer, responses={200: TicketSerializer()})
    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})
        try:
            user = Ticket.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exist"})
        event_id = request.data['event']
        user_id = request.data['user']
        user_exists = User.objects.filter(pk=user_id).exists()
        event_exists = Event.objects.filter(pk=event_id).exists()
        if not user_exists:
            return Response({"error": f"There is no user with {str(user_id)}"})
        if not event_exists:
            return Response({"error": f"There is no event with {str(event_id)}"})
        serializer = TicketSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={200: "Object deleted successfully"})
    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"ERROR": "Delete Method Is Not Allowed"})

        # deleting an object from api

        try:
            instance = Ticket.objects.get(pk=pk)
            instance.delete()
        except:
            return Response({"ERROR": "Object Not Found !"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"post": f"Object {str(pk)} is deleted"})


