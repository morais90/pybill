# -*- coding: utf-8 -*-
from django_filters import rest_framework as filters
from .models import Bill


class BillFilter(filters.FilterSet):
    subscriber = filters.CharFilter(field_name='start_record__source')
    period_year = filters.NumberFilter(field_name='end_record__timestamp__year')
    period_month = filters.NumberFilter(field_name='end_record__timestamp__month')

    class Meta:
        model = Bill
        fields = ('subscriber', 'period_year', 'period_month')
