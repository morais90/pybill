# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CallRecord, Bill


@receiver(post_save, sender=CallRecord)
def call_record_post_save_handler(sender, instance, created, **kwargs):
    if created:
        instance_is_start_record = instance.type == CallRecord.START_RECORD

        pair_type = CallRecord.END_RECORD if instance_is_start_record else CallRecord.START_RECORD
        pair = CallRecord.objects.filter(call_id=instance.call_id, type=pair_type).first()

        if pair:
            start_record, end_record = (instance, pair) if instance_is_start_record else (pair, instance)
            Bill.objects.create(start_record=start_record, end_record=end_record)
