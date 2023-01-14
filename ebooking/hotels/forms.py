from .models import Reservation

class ReservationForm():
    class Meta:
        model = Reservation
        exclude = ()