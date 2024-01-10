from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Event, Ticket
from datetime import datetime

class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {'username': 'testuser', 'email': 'test@example.com'}

    def test_create_user(self):
        response = self.client.post('/api/user/', self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_get_all_users(self):
        response = self.client.get('/api/user/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Перевірте, чи маємо JSON відповідь
        # self.assertEqual(response['Content-Type'], 'application/json')
        #
        # # Перевірте довжину JSON-даних
        # data = response.json()
        # self.assertEqual(len(data), User.objects.count())

    def test_get_single_user(self):
        user = User.objects.create(username='testuser', email='test@example.com')
        response = self.client.get(f'/api/user/{user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_update_user(self):
        user = User.objects.create(username='testuser', email='test@example.com')
        updated_data = {'username': 'newuser', 'email': 'new@example.com'}
        response = self.client.put(f'/api/user/{user.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(id=user.id).username, 'newuser')

    def test_delete_user(self):
        user = User.objects.create(username='testuser', email='test@example.com')
        response = self.client.delete(f'/api/user/{user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 0)

class EventAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.event_data = {'name': 'Test Event', 'date': '2023-12-31', 'location': 'Test Location', 'price': 20.0}

    def test_create_event(self):
        response = self.client.post('/api/event/', self.event_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(Event.objects.get().name, 'Test Event')

    def test_get_all_events(self):
        response = self.client.get('/api/event/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), Event.objects.count())

    def test_get_single_event(self):
        event = Event.objects.create(name='Test Event', date='2023-12-31', location='Test Location', price=20.0)
        response = self.client.get(f'/api/event/{event.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Event')

    def test_update_event(self):
        event = Event.objects.create(name='Test Event', date='2023-12-31', location='Test Location', price=20.0)
        updated_data = {'name': 'Updated Event', 'date': '2023-12-31', 'location': 'Updated Location', 'price': 25.0}
        response = self.client.put(f'/api/event/{event.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.get(id=event.id).name, 'Updated Event')

    def test_delete_event(self):
        event = Event.objects.create(name='Test Event', date='2023-12-31', location='Test Location', price=20.0)
        response = self.client.delete(f'/api/event/{event.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Event.objects.count(), 0)


class TicketAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username='testuser', email='test@example.com')
        event = Event.objects.create(name='Test Event', date='2023-12-31', location='Test Location', price=20.0)
        self.ticket_data = {'user': user.id, 'event': event.id, 'purchase_date': '2023-12-30'}

    def test_create_ticket(self):
        response = self.client.post('/api/ticket/', self.ticket_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 1)

    def test_get_all_tickets(self):
        response = self.client.get('/api/ticket/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data), Ticket.objects.count())

    def test_get_single_ticket(self):
        ticket = Ticket.objects.create(
            user=User.objects.get(username='testuser'),
            event=Event.objects.get(name='Test Event'),
            purchase_date='2023-12-30'
        )
        response = self.client.get(f'/api/ticket/{ticket.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], ticket.user.id)
        self.assertEqual(response.data['event'], ticket.event.id)

    def test_update_ticket(self):
        ticket = Ticket.objects.create(
            user=User.objects.get(username='testuser'),
            event=Event.objects.get(name='Test Event'),
            purchase_date='2023-12-30'
        )
        updated_data = {'user': ticket.user.id, 'event': ticket.event.id, 'purchase_date': '2023-12-09'}
        response = self.client.put(f'/api/ticket/{ticket.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Замініть рядок нижче на об'єкт datetime
        expected_date = ticket.event.date
        actual_datetime = Ticket.objects.get(id=ticket.id).purchase_date

        # Порівняти лише дату
        self.assertGreaterEqual(expected_date, actual_datetime.date())

    def test_delete_ticket(self):
        ticket = Ticket.objects.create(
            user=User.objects.get(username='testuser'),
            event=Event.objects.get(name='Test Event'),
            purchase_date='2023-12-30'
        )
        response = self.client.delete(f'/api/ticket/{ticket.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Ticket.objects.count(), 0)