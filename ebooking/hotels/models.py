from django.db import models

# Create your models here.

class HotelRoom(models.Model):
    image = models.ImageField(upload_to='hotelroom/', null=True)
    beds = models.IntegerField()
    has_terrace = models.BooleanField(default=True)
    has_kitchen = models.BooleanField(default=True)
    has_tv = models.BooleanField(default=True)
    has_fridge = models.BooleanField(default=True)
    floor_no = models.PositiveIntegerField()

class Hotel(models.Model):
    image = models.ImageField(upload_to='hotel/', null=True)
    name = models.CharField(max_length=50, null=False)
    stars= models.PositiveIntegerField(null=False)
    hotelRooms = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, null=True) # oneToMany
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

class Reservation(models.Model):
    hotelRoom = models.ForeignKey(HotelRoom, on_delete=models.CASCADE, null=True) # oneToMany
    begin_at = models.DateTimeField(null=False)
    ends_at = models.DateTimeField(null=False)
    time_in_days = models.PositiveIntegerField(null=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name  