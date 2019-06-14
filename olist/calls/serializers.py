# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import CallRecord


class CallRecordStartSerializer(serializers.ModelSerializer):
    source = serializers.CharField(min_length=10, max_length=11, allow_blank=False)
    destination = serializers.CharField(min_length=10, max_length=11, allow_blank=False)

    def validate_source(self, data):
        # TODO validate area code and starts digits
        if not data.isdigit():
            raise serializers.ValidationError('Ensure this field is a phone number with area code.')

        return data

    def validate_destination(self, data):
        # TODO validate area code and starts digits
        if not data.isdigit():
            raise serializers.ValidationError('Ensure this field is a phone number with area code.')

        return data

    def validate(self, data):
        self._validate_source_destination(data)
        self._validate_timestamp(data)

        return data

    def _validate_source_destination(self, data):
        source = data.get('source')
        destination = data.get('destination')

        if source == destination:
            raise serializers.ValidationError({
                'source': ['This field should be different from destination.'],
                'destination': ['This field should be different from source.']
            })

    def _validate_timestamp(self, data):
        call_id = data.get('call_id')
        timestamp = data.get('timestamp')
        end_record = CallRecord.objects.filter(call_id=call_id, type=CallRecord.END_RECORD).first()

        if end_record and timestamp > end_record.timestamp:
            raise serializers.ValidationError({
                'timestamp': ['Ensure this field is less than the end record timestamp']
            })

    class Meta:
        model = CallRecord
        fields = '__all__'


class CallRecordEndSerializer(serializers.ModelSerializer):
    def validate(self, data):
        self._validate_timestamp(data)

        return data

    def _validate_timestamp(self, data):
        call_id = data.get('call_id')
        timestamp = data.get('timestamp')
        start_record = CallRecord.objects.filter(call_id=call_id, type=CallRecord.START_RECORD).first()

        if start_record and timestamp < start_record.timestamp:
            raise serializers.ValidationError({
                'timestamp': ['Ensure this field is greater than the start record timestamp']
            })

    class Meta:
        model = CallRecord
        fields = ('id', 'timestamp', 'call_id', 'type')
