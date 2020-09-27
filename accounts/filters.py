from django_filters import FilterSet
from django_filters import DateFilter

from .models import Order

class OrderFilter(FilterSet):
    start_date = DateFilter(field_name='date_created', lookup_expr='gte', label='Start Date ')
    end_date = DateFilter(field_name='date_created', lookup_expr='lte', label='End Date ')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']