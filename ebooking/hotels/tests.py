from django.test import TestCase
import unittest
from django.contrib.auth import get_user_model
from .models import Hotel, Review, HotelRoom
from django.test import TestCase, Client
from django.urls import reverse
from hotels.models import Hotel, HotelRoom, Review
from accounts.models import User, Profile
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class HotelTestCase(TestCase):
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
            has_breakfast=True
        )
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
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
        self.review = Review.objects.create(
            hotel=self.hotel,
            user=self.user,
            rating=4,
            text='Test review'
        )

    def test_average_rating(self):
        # Test when there is only one review
        self.assertEqual(self.hotel.average_rating, 4)

        # Test when there are multiple reviews
        Review.objects.create(
            hotel=self.hotel,
            user=self.user,
            rating=3,
            text='Another test review'
        )
        self.assertEqual(self.hotel.average_rating, 3.5)

        # Test when there are no reviews
        Review.objects.all().delete()
        self.assertEqual(self.hotel.average_rating, 0)

    def test_str(self):
        self.assertEqual(str(self.hotel), 'Test Hotel')
        
    def test_hotel_room_relationship(self):
        self.assertEqual(self.hotel.hotelroom.count(), 1)
        self.assertEqual(self.hotel_room.hotel, self.hotel)

class HotelRoomTestCase(TestCase):
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
            has_breakfast=True
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

    def test_str(self):
        expected_string = "Camera hotel: Test Hotel cu nr.paturi :2 pret: 200  la etajul: 1"
        self.assertEqual(str(self.hotel_room), expected_string)

    def test_default_values(self):
        self.assertEqual(self.hotel_room.has_terrace, True)
        self.assertEqual(self.hotel_room.has_kitchen, True)
        self.assertEqual(self.hotel_room.has_tv, True)
        self.assertEqual(self.hotel_room.has_fridge, True)
        self.assertEqual(self.hotel_room.price, 200)


class ReviewTestCase(TestCase):
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
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        profile = Profile.objects.create(user=self.user, phone="123456")
        self.user.profile = profile
        self.user.save()
        self.review = Review.objects.create(
            hotel=self.hotel,
            user=self.user,
            rating=4,
            text='Test review'
        )

    def test_str(self):
        self.assertEqual(str(self.review), 'Test Hotel - 4')

    def test_hotel_relationship(self):
        self.assertEqual(self.review.hotel, self.hotel)

    def test_user_relationship(self):
        self.assertEqual(self.review.user, self.user)

    def test_rating_value(self):
        self.assertLessEqual(self.review.rating, 5)
        self.assertGreaterEqual(self.review.rating, 1)


# Testing views



class HotelViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='testuser@test.com', password='testpass', username='testuser')
        profile = Profile.objects.create(user=self.user, phone="123456")
        self.user.profile = profile
        self.user.save()
        img = SimpleUploadedFile(
                'tests/image.jpg', 
                content=b'', 
                content_type='image/jpg'
        )
        self.hotel = Hotel.objects.create(name='Test Hotel', city='Test City', region='Test Region',
                                           country='Test Country', zone='Test Zone', rooms=2, floors=3,
                                           parking_places=10, restaurant_places=20, has_wifi=True,
                                           has_breakfast=True, image=img)

    def test_hotel_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_hotel_detail_view(self):
        response = self.client.get(reverse('user_hotel_rooms', args=[self.hotel.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rent_rooms.html')


class HotelRoomTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(email='testuser@test.com', password='testpass', username='testuser')
        profile = Profile.objects.create(user=self.user, phone="123456")
        self.user.profile = profile
        self.user.save()
        img = SimpleUploadedFile(
                'tests/image.jpg', 
                content=b'', 
                content_type='image/jpg'
        )  
        self.hotel = Hotel.objects.create(name='Test Hotel', city='Test City', region='Test Region',
                                           country='Test Country', zone='Test Zone', rooms=2, floors=3,
                                           parking_places=10, restaurant_places=20, has_wifi=True,
                                           has_breakfast=True, image=img)
        self.hotel_room = HotelRoom.objects.create(hotel=self.hotel, beds=2, has_terrace=True,
                                                   has_kitchen=True, has_tv=True, has_fridge=True,
                                                   floor_no=1, price=100, image=img)

    def test_list_hotel_rooms_view(self):
        response = self.client.get(reverse('user_hotel_rooms', args=[self.hotel.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'rent_rooms.html')

    def test_create_hotel_room_view(self):
        self.client.login(email='testuser@test.com', password='testpass', username='usertest')
        response = self.client.post(reverse('add_room', args=[self.hotel.id]), {
            'beds': 3,
            'has_terrace': True,
            'has_kitchen': True,
            'has_tv': True,
            'has_fridge': True,
            'floor_no': 2,
            'price': 150,
        })
        self.assertEqual(response.status_code, 302)

    def test_update_hotel_room_view(self):
        self.client.login(email='testuser@test.com', password='testpass')
        response = self.client.post(reverse('edit_room', args=[self.hotel.id, self.hotel_room.id]), {
            'beds': 3,
            'has_terrace': True,
            'has_kitchen': True,
            'has_tv': True,
            'has_fridge': True,
            'floor_no': 2,
            'price': 150,
        })
        self.assertEqual(response.status_code, 403)

    def test_delete_hotel_room_view(self):
        self.client.login(email='testuser@test.com', password='testpass', username='usertest')
        response = self.client.post(reverse('delete_room', args=[self.hotel.id, self.hotel_room.id]))
        self.assertEqual(response.status_code, 302)