from django.test import TestCase
from django.test import Client
from .models import Hotel

# Create your tests here.

class HotelModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Hotel.objects.create(name='Marriot', stars=5, city='Bucharest', region="Muntenia", country="Romania", zone="Ilfov", floors=5, parking_places=50, restaurant_places=2, has_wifi=True, has_breakfast=False)

    def test_hotel_name_label(self):
        hotel = Hotel.objects.get(id=1)
        field_label = hotel._meta.get_field('has_wifi').verbose_name
        self.assertEqual(field_label, 'wifi')

    def test_hotel_stars_label(self):
        hotel = Hotel.objects.get(id=1)
        field_label = hotel._meta.get_field('has_breakfast').verbose_name
        self.assertEqual(field_label, 'breakfast')     


    def test_get_absolute_url(self):
        hotel = Hotel.objects.get(id=1)
        self.assertEqual(hotel.get_absolute_url(), '/hotel/1')

    def test_hotel_str(self):
        hotel = Hotel.objects.get(name="Marriot")
        self.assertEqual(str(hotel), "Marriot")

    def test_hotel_fields(self):
        hotel = Hotel.objects.get(id=1)
        expected_fields = [
            ("ID", hotel.id),
            ("image", hotel.image),
            ("name", hotel.name),
            ("stars", hotel.stars),
            ("city", hotel.city),
            ("region", hotel.region),
            ("country", hotel.country),
            ("zone", hotel.zone),
            ("rooms", hotel.rooms),
            ("floors", hotel.floors),
            ("parking places", hotel.parking_places),
            ("restaurant places", hotel.restaurant_places),
            ("wifi", hotel.has_wifi),
            ("breakfast", hotel.has_breakfast),
        ]
        self.assertEqual(hotel.get_fields(), expected_fields)

    def test_hotel_defaults(self):
        hotel = Hotel.objects.create(
            name="Rin",
            stars=4,
            city="Bucharest",
            region="Muntenia",
            country="RO",
            parking_places=50,
            restaurant_places=1,
            floors = 5,
            zone="IF",
        )
        self.assertEqual(hotel.rooms, 1)
        self.assertEqual(hotel.has_wifi, True)
        self.assertEqual(hotel.has_breakfast, False)    