import django_filters
from django import forms
from django.forms import TextInput
from django_filters import DateFilter, CharFilter, ModelChoiceFilter
from django_filters.widgets import *
import datetime
from .models import Reservation
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseFilter(django_filters.FilterSet):
    begin_at = DateFilter(field_name='data_crearii',
                            widget=forms.DateInput(
                                attrs={'class': 'form-control mydate', 'type': 'date'}),
                            method='filter_start_range', label='De la')
    ends_at = DateFilter(field_name='data_expirarii',
                          widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                          method='filter_end_range', label='Până la')

    def filter_start_range(self, queryset, name, value):
        filtered_qs = queryset.filter(data_crearii__gte=value)
        return filtered_qs

    def filter_end_range(self, queryset, name, value):
        value += datetime.timedelta(days=1)
        filtered_qs = queryset.filter(data_crearii__lte=value)
        return filtered_qs



# Filter used by staff

class HotelNameFilter(CharFilter):
    field_class = forms.CharField
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('lookup_expr', 'icontains')  # set the lookup expression
        kwargs.setdefault('label', 'Hotel Name')
        kwargs.setdefault('widget', forms.TextInput(attrs={'placeholder': 'Enter hotel name'}))
        super().__init__(*args, **kwargs)

class ReservationFilter(BaseFilter):
    hotel_name = HotelNameFilter(field_name='hotelRoom__hotel__name')

    class Meta:
        model = Reservation
        fields = {
            'first_name': ['icontains'],
            'last_name': ['icontains'],
            'phone_no': ['exact'],
        }