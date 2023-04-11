from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.

class Hotel(models.Model):
    image = models.ImageField(upload_to='hotel/', null=True)
    name = models.CharField(max_length=50, null=False)    
    city = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zone = models.CharField(max_length=50)
    rooms = models.PositiveIntegerField(default=1) # Maybe add some default values 
    floors = models.PositiveIntegerField() # Maybe add some default values 
    parking_places = models.PositiveIntegerField() # Maybe add some default values 
    restaurant_places = models.PositiveIntegerField() # Maybe add some default values 
    has_wifi = models.BooleanField()  # Maybe add some default values  
    has_breakfast = models.BooleanField() # Maybe add some default values

    def __str__(self) -> str:
        return self.name

    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            total_rating = sum([review.rating for review in reviews])
            return round(total_rating / len(reviews), 1)
        return 0
    class Meta:
        db_table = 'hotel'


class HotelRoom(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='hotelroom', null=True)
    image = models.ImageField(upload_to='hotelroom/', null=True)
    beds = models.IntegerField()
    has_terrace = models.BooleanField(default=True)
    has_kitchen = models.BooleanField(default=True)
    has_tv = models.BooleanField(default=True)
    has_fridge = models.BooleanField(default=True)
    floor_no = models.PositiveIntegerField()
    price = models.PositiveIntegerField(default=100, null=True)

    class Meta:
        db_table = 'hotelroom'

    def __str__(self) -> str:
        return "Camera hotel: " + self.hotel.name + " cu nr.paturi :" + str(self.beds) + " pret: " + str(self.price) + "  la etajul: " + str(self.floor_no)
    

class Review(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    text = models.TextField()
    
    def __str__(self) -> str:
        return f'{self.hotel.name} - {self.rating}'
  