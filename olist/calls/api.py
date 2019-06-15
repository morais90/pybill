# -*- coding: utf-8 -*-
import pendulum
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import exceptions

from .models import CallRecord, Bill
from .serializers import CallRecordStartSerializer, CallRecordEndSerializer, BillSerializer
from .filters import BillFilter


class CallRecordViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CallRecord.objects.all()

    def get_serializer_class(self):
        data = self.request.data

        if data.get('type') == CallRecord.START_RECORD:
            return CallRecordStartSerializer
        return CallRecordEndSerializer


class BillViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = BillSerializer
    filter_class = BillFilter

    def get_queryset(self):
        return Bill.objects.filter(
            end_record__timestamp__lt=pendulum.now().start_of('month')
        ).select_related(
            'start_record',
            'end_record'
        )

    def filter_queryset(self, queryset):
        self._check_or_set_period_params(queryset)

        return super().filter_queryset(queryset)

    def _check_or_set_period_params(self, queryset):
        period_year = self.request.query_params.get('period_year')
        period_month = self.request.query_params.get('period_month')

        if not period_year and period_month:
            raise exceptions.ValidationError({
                'period_year': ['Ensure that this field is filled.']
            })

        if not period_month and period_year:
            raise exceptions.ValidationError({
                'period_month': ['Ensure that this field is filled.']
            })

        if not period_year and not period_month:
            self._set_period_params(queryset)

    def _set_period_params(self, queryset):
        subscriber = self._get_subscriber_param()
        last_bill = queryset.filter(start_record__source=subscriber)

        if last_bill.exists():
            last_bill = last_bill.latest('end_record__timestamp')
            last_period = last_bill.end_record.timestamp

            query_params = self.request.query_params.copy()
            query_params['period_year'] = last_period.year
            query_params['period_month'] = last_period.month

            self.request._request.GET = query_params

    def _get_subscriber_param(self):
        subscriber = self.request.query_params.get('subscriber')

        if not subscriber:
            raise exceptions.ValidationError({'subscriber': ['This query parameter is required.']})

        return subscriber
