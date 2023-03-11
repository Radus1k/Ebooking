from django.db import models

# Create your models here.

class Hotel(models.Model):
    image = models.ImageField(upload_to='hotel/', null=True)
    name = models.CharField(max_length=50, null=False)
    stars= models.PositiveIntegerField(null=False)
    
    city = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    zone = models.CharField(max_length=50)
    rooms = models.PositiveIntegerField(default=1) # Maybe add some default values 
    floors = models.PositiveIntegerField() # Maybe add some default values 
    parking_places = models.PositiveIntegerField() # Maybe add some default values 
    restaurant_places = models.PositiveIntegerField() # Maybe add some default values 
    has_wifi = models.BooleanField(verbose_name='wifi',default=True)  # Maybe add some default values  
    has_breakfast = models.BooleanField(verbose_name='breakfast',default=False) # Maybe add some default values

    def __str__(self) -> str:
        return self.name
    
    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self)) for field in self.__class__._meta.fields]

    def get_absolute_url(self):
        return f'/hotel/{self.id}'

    class Meta:
        db_table = 'hotel'




class HotelRoom(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='hotelroom', null=True)
    image = models.ImageField(upload_to='hotelroom/', null=True)
    beds = models.IntegerField()
    has_terrace = models.BooleanField(default=True, verbose_name='terrace')
    has_kitchen = models.BooleanField(default=True, verbose_name='kitchen')
    has_tv = models.BooleanField(default=True, verbose_name='tv')
    has_fridge = models.BooleanField(default=True, verbose_name='fridge')
    floor_no = models.PositiveIntegerField()
    price = models.PositiveIntegerField(default=100, null=True)

    class Meta:
        db_table = 'hotelroom'
