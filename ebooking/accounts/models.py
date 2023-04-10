from django.db import models
from django.contrib.auth import get_user_model
from hotels.models import Hotel

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=30)
    is_hotel_administrator = models.BooleanField(default=False)
    hotels = models.ManyToManyField(Hotel, blank=True)

    def __str__(self):
        return self.user.email

    