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
