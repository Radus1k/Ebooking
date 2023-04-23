from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from hotels.models import Hotel, HotelRoom
from .models import Reservation
import datetime
from django.urls import reverse
from reservation.models import Reservation
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class ReservationModelTestCase(TestCase):
    def setUp(self):
        self.hotel = Hotel.objects.create(
            name='Test Hotel',
            city='Test City',
            region='Test Region',
            country='Test Country',
            zone='Test Zone',
            rooms=10,
            floors=5,
            parking_places=20,
            restaurant_places=50,
            has_wifi=True,
            has_breakfast=True,
            image=SimpleUploadedFile(
                'tests/image.jpg', 
                content=b'', 
                content_type='image/jpg'
            )
        )
        self.hotel_room = HotelRoom.objects.create(
            hotel=self.hotel,
            beds=2,
            has_terrace=True,
            has_kitchen=True,
            has_tv=True,
            has_fridge=True,
            floor_no=1,
            price=200
        )
        self.user = User.objects.create_user(
            email='test@test.com',
            username='testuser',
            password='password',
            first_name='Test',
            last_name='User'
        )
        self.reservation = Reservation.objects.create(
            hotelRoom=self.hotel_room,
            user=self.user,
            begin_at=datetime.datetime.now(),
            ends_at=datetime.datetime.now() + datetime.timedelta(days=1),
            phone_no='123456789',
            first_name='John',
            last_name='Doe',
            observations='Test Observations',
            status='In asteptare'
        )

    def test_reservation_duration_in_days(self):
        reservation = self.reservation
        self.assertEqual(reservation.duration_in_days(), 1)

    def test_reservation_str_method(self):
        reservation = self.reservation
        expected_result = 'Test User reservation at Test Hotel at Camera hotel: Test Hotel cu nr.paturi :2 pret: 200  la etajul: 1'
        self.assertEqual(str(reservation), expected_result)

    def test_reservation_status_choices(self):
        reservation = self.reservation
        choices = [choice[0] for choice in reservation.STATUS_CHOICES]
        self.assertListEqual(choices, ['In asteptare', 'Confirmata', 'Anulata'])

# Test views

class ReservationViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='testpass')
        self.hotel = Hotel.objects.create(
            name='Test Hotel',
            city='Test City',
            region='Test Region',
            country='Test Country',
            zone='Test Zone',
            rooms=10,
            floors=5,
            parking_places=20,
            restaurant_places=50,
            has_wifi=True,
            has_breakfast=True,
            image=SimpleUploadedFile(
                'tests/image.jpg', 
                content=b'', 
                content_type='image/jpg'
            )
        )
        self.hotel_room = HotelRoom.objects.create(
            hotel=self.hotel,
            beds=2,
            has_terrace=True,
            has_kitchen=True,
            has_tv=True,
            has_fridge=True,
            floor_no=1,
            price=200
        )
        self.url = reverse('reservation:reservation', args=[self.hotel_room.id])

    def test_reservation_view_GET(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reservation.html')
        self.assertContains(response, 'Creaza o rezervare')

    def test_reservation_view_POST(self):
        self.client.force_login(self.user)
        data = {
            'begins_at': '2023-05-01',
            'ends_at': '2023-05-03',
            'first_name':'Radu',
            'last_name':'Marius',

        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reservation.objects.count(), 0)