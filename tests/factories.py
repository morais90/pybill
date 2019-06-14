# -*- coding: utf-8 -*-
import factory
from datetime import timedelta
from django.utils import timezone

from olist.calls.models import CallRecord


class CallRecordStartFactory(factory.django.DjangoModelFactory):
    type = CallRecord.START_RECORD
    timestamp = timezone.now()
    call_id = 1
    source = '4899994444'
    destination = '48889988001'

    class Meta:
        model = CallRecord


class CallRecordEndFactory(factory.django.DjangoModelFactory):
    type = CallRecord.END_RECORD
    timestamp = timezone.now() + timedelta(hours=3)
    call_id = 1

    class Meta:
        model = CallRecord
