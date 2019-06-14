# -*- coding: utf-8 -*-
from django.utils import dateparse
from rest_framework.test import APITransactionTestCase
from rest_framework import status

from olist.calls.models import CallRecord
from tests.factories import CallRecordStartFactory, CallRecordEndFactory


class CallRecordCreate(APITransactionTestCase):
    reset_sequences = True

    def test_create_start_record(self):
        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.START_RECORD,
                'timestamp': '2016-02-29T12:00:00Z',
                'source': '99988526423',
                'destination': '9933468278'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.json(), {
            'id': 1,
            'type': 0,
            'timestamp': '2016-02-29T12:00:00Z',
            'call_id': '1',
            'source': '99988526423',
            'destination': '9933468278'
        })

    def test_create_start_record_with_already_created_end_record(self):
        CallRecordEndFactory.create(call_id=1)

        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.START_RECORD,
                'timestamp': '2016-02-29T12:00:00Z',
                'source': '99988526423',
                'destination': '9933468278'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.json(), {
            'id': 2,
            'type': 0,
            'timestamp': '2016-02-29T12:00:00Z',
            'call_id': '1',
            'source': '99988526423',
            'destination': '9933468278'
        })

    def test_create_end_record(self):
        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.END_RECORD,
                'timestamp': '2016-02-29T14:00:00Z'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.json(), {
            'id': 1,
            'type': 1,
            'timestamp': '2016-02-29T14:00:00Z',
            'call_id': '1'
        })

    def test_create_end_record_with_already_start_record_created(self):
        CallRecordStartFactory.create(call_id=1, timestamp=dateparse.parse_datetime('2016-02-29T12:00:00Z'))

        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.END_RECORD,
                'timestamp': '2016-02-29T14:00:00Z'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictEqual(response.json(), {
            'id': 2,
            'type': 1,
            'timestamp': '2016-02-29T14:00:00Z',
            'call_id': '1'
        })

    def test_create_start_record_call_id_duplicated(self):
        CallRecordStartFactory.create(call_id=1)

        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.START_RECORD,
                'timestamp': '2016-02-29T12:00:00Z',
                'source': '99988526423',
                'destination': '9933468278'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'non_field_errors': ['The fields type, call_id must make a unique set.']
        })

    def test_create_end_record_call_id_duplicated(self):
        CallRecordEndFactory.create(call_id=1)

        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.END_RECORD,
                'timestamp': '2016-02-29T12:00:00Z'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'non_field_errors': ['The fields type, call_id must make a unique set.']
        })

    def test_create_type_required(self):
        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'timestamp': '2016-02-29T12:00:00Z'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'type': ['This field is required.']
        })

    def test_create_type_null(self):
        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'timestamp': '2016-02-29T12:00:00Z',
                'type': None
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'type': ['This field may not be null.']
        })

    def test_create_type_invalid_choice(self):
        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'timestamp': '2016-02-29T12:00:00Z',
                'type': 99
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'type': ['"99" is not a valid choice.']
        })

    def test_create_start_record_source_required(self):
        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.START_RECORD,
                'timestamp': '2016-02-29T12:00:00Z',
                'destination': '9933468278'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'source': ['This field is required.']
        })

    def test_create_start_record_source_blank(self):
        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.START_RECORD,
                'timestamp': '2016-02-29T12:00:00Z',
                'source': '',
                'destination': '9933468278'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'source': ['This field may not be blank.']
        })

    def test_create_start_record_source_null(self):
        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.START_RECORD,
                'timestamp': '2016-02-29T12:00:00Z',
                'source': None,
                'destination': '9933468278'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'source': ['This field may not be null.']
        })

    def test_create_start_record_source_min_length(self):
        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.START_RECORD,
                'timestamp': '2016-02-29T12:00:00Z',
                'source': '9',
                'destination': '9933468278'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'source': ['Ensure this field has at least 10 characters.']
        })

    def test_create_start_record_source_max_length(self):
        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.START_RECORD,
                'timestamp': '2016-02-29T12:00:00Z',
                'source': '999885264231',
                'destination': '9933468278'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'source': ['Ensure this field has no more than 11 characters.']
        })

    def test_create_start_record_source_not_phone(self):
        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.START_RECORD,
                'timestamp': '2016-02-29T12:00:00Z',
                'source': 'AA988526423',
                'destination': '9933468278'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'source': ['Ensure this field is a phone number with area code.']
        })

    def test_create_start_record_destination_required(self):
        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.START_RECORD,
                'timestamp': '2016-02-29T12:00:00Z',
                'source': '99988526423'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'destination': ['This field is required.']
        })

    def test_create_start_record_destination_blank(self):
        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.START_RECORD,
                'timestamp': '2016-02-29T12:00:00Z',
                'source': '99988526423',
                'destination': ''
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'destination': ['This field may not be blank.']
        })

    def test_create_start_record_destination_null(self):
        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.START_RECORD,
                'timestamp': '2016-02-29T12:00:00Z',
                'source': '99988526423',
                'destination': None
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'destination': ['This field may not be null.']
        })

    def test_create_start_record_destination_min_length(self):
        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.START_RECORD,
                'timestamp': '2016-02-29T12:00:00Z',
                'source': '99988526423',
                'destination': '9'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'destination': ['Ensure this field has at least 10 characters.']
        })

    def test_create_start_record_destination_max_length(self):
        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.START_RECORD,
                'timestamp': '2016-02-29T12:00:00Z',
                'source': '99988526423',
                'destination': '993346827811'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'destination': ['Ensure this field has no more than 11 characters.']
        })

    def test_create_start_record_source_equal_destination(self):
        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.START_RECORD,
                'timestamp': '2016-02-29T12:00:00Z',
                'source': '99988526423',
                'destination': '99988526423'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'source': ['This field should be different from destination.'],
            'destination': ['This field should be different from source.']
        })

    def test_create_start_record_timestamp_greater_than_end_record(self):
        timestamp = dateparse.parse_datetime('2016-02-29T12:00:00Z')
        CallRecordEndFactory.create(timestamp=timestamp)

        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.START_RECORD,
                'timestamp': '2016-02-29T12:00:01Z',
                'source': '99988526423',
                'destination': '9933468278'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'timestamp': ['Ensure this field is less than the end record timestamp'],
        })

    def test_create_end_record_timestamp_less_than_start_record(self):
        timestamp = dateparse.parse_datetime('2016-02-29T12:00:01Z')
        CallRecordStartFactory.create(timestamp=timestamp)

        response = self.client.post(
            '/call-record/',
            {
                'call_id': 1,
                'type': CallRecord.END_RECORD,
                'timestamp': '2016-02-29T12:00:00Z'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'timestamp': ['Ensure this field is greater than the start record timestamp'],
        })
