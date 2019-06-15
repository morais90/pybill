# -*- coding: utf-8 -*-
import pendulum
from decimal import Decimal
from django.db import models


class CallRecord(models.Model):
    START_RECORD = 0
    END_RECORD = 1
    TYPES = (
        (START_RECORD, 'Start record'),
        (END_RECORD, 'End record')
    )

    type = models.IntegerField(choices=TYPES)
    timestamp = models.DateTimeField()
    call_id = models.CharField(max_length=256)
    source = models.CharField(max_length=11, blank=True)
    destination = models.CharField(max_length=11, blank=True)

    class Meta:
        unique_together = ('type', 'call_id')


class Bill(models.Model):
    STANDING_CHARGE = Decimal('0.36')
    CALL_CHARGE = Decimal('0.09')
    REDUCED_HOURS = (pendulum.time(22), pendulum.time(6))

    start_record = models.ForeignKey(CallRecord, related_name='start_record_bill', on_delete=models.CASCADE)
    end_record = models.ForeignKey(CallRecord, related_name='end_record_bill', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def start_date(self):
        return self.start_record.timestamp.date()

    @property
    def start_time(self):
        return self.start_record.timestamp.time()

    @property
    def duration(self):
        start_date = pendulum.instance(self.start_record.timestamp)
        end_date = pendulum.instance(self.end_record.timestamp)

        return (end_date - start_date)

    def _calculate_price(self):
        price = Decimal('0.0')
        start_date = pendulum.instance(self.start_record.timestamp)
        end_date = pendulum.instance(self.end_record.timestamp)
        period = pendulum.period(start_date, end_date)

        if period.total_minutes() >= 1:
            min_reduced_hour, max_reduced_hour = self.REDUCED_HOURS

            for date in period.range('minutes'):
                time = date.time()

                if time >= min_reduced_hour or time <= max_reduced_hour:
                    continue

                if date == start_date:
                    # period.range is inclusive. We only compute complete cycles of
                    # minutes.
                    continue
                price += Decimal('0.09')
            price += self.STANDING_CHARGE

        return price.quantize(Decimal('0.01'))

    def save(self, *args, **kwargs):
        self.price = self._calculate_price()

        return super().save(*args, **kwargs)
