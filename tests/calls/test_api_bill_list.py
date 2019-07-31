# -*- coding: utf-8 -*-
import pendulum
from unittest.mock import patch
from rest_framework.test import APITransactionTestCase
from rest_framework import status

from pybill.calls.models import CallRecord


class BillListTestCase(APITransactionTestCase):
    reset_sequences = True

    def setUp(self):
        sample_data = {
            '70': {
                'source': '99988526423',
                'destination': '9933468278',
                'start_timestamp': '2016-02-29T12:00:00Z',
                'end_timestamp': '2016-02-29T14:00:00Z'
            },
            '71': {
                'source': '99988526423',
                'destination': '9933468278',
                'start_timestamp': '2017-12-11T15:07:13Z',
                'end_timestamp': '2017-12-11T15:14:56Z'
            },
            '72': {
                'source': '99988526423',
                'destination': '9933468278',
                'start_timestamp': '2017-12-12T22:47:56Z',
                'end_timestamp': '2017-12-12T22:50:56Z'
            },
            '73': {
                'source': '99988526423',
                'destination': '9933468278',
                'start_timestamp': '2017-12-12T21:57:13Z',
                'end_timestamp': '2017-12-12T22:10:56Z'
            },
            '74': {
                'source': '99988526423',
                'destination': '9933468278',
                'start_timestamp': '2017-12-12T04:57:13Z',
                'end_timestamp': '2017-12-12T06:10:56Z'
            },
            '75': {
                'source': '99988526423',
                'destination': '9933468278',
                'start_timestamp': '2017-12-13T21:57:13Z',
                'end_timestamp': '2017-12-14T22:10:56Z'
            },
            '76': {
                'source': '99988526423',
                'destination': '9933468278',
                'start_timestamp': '2017-12-12T15:07:58Z',
                'end_timestamp': '2017-12-12T15:12:56Z'
            },
            '77': {
                'source': '99988526423',
                'destination': '9933468278',
                'start_timestamp': '2018-02-28T21:57:13Z',
                'end_timestamp': '2018-03-01T22:10:56Z'
            }
        }

        for call_id, sample in sample_data.items():
            start_timestamp = sample.pop('start_timestamp')
            end_timestamp = sample.pop('end_timestamp')

            CallRecord.objects.create(
                type=CallRecord.START_RECORD,
                call_id=call_id,
                timestamp=pendulum.parse(start_timestamp),
                **sample
            )
            CallRecord.objects.create(
                type=CallRecord.END_RECORD,
                call_id=call_id,
                timestamp=pendulum.parse(end_timestamp)
            )

    @patch('pendulum.now', return_value=pendulum.datetime(2018, 1, 1))
    def test_list_bill_filter_by_previous_month(self, now_mock):
        response = self.client.get(
            '/bill/',
            {'subscriber': '99988526423'}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.json(), [
            {
                'id': 2,
                'start_date': '2017-12-11',
                'start_time': '15:07:13',
                'duration': '00:07:43',
                'price': '0.99'
            },
            {
                'id': 3,
                'start_date': '2017-12-12',
                'start_time': '22:47:56',
                'duration': '00:03:00',
                'price': '0.36'
            },
            {
                'id': 4,
                'start_date': '2017-12-12',
                'start_time': '21:57:13',
                'duration': '00:13:43',
                'price': '0.54'
            },
            {
                'id': 5,
                'start_date': '2017-12-12',
                'start_time': '04:57:13',
                'duration': '01:13:43',
                'price': '1.35'
            },
            {
                'id': 6,
                'start_date': '2017-12-13',
                'start_time': '21:57:13',
                'duration': '1 00:13:43',
                'price': '86.94'
            },
            {
                'id': 7,
                'start_date': '2017-12-12',
                'start_time': '15:07:58',
                'duration': '00:04:58',
                'price': '0.72'
            }
        ])

    @patch('pendulum.now', return_value=pendulum.datetime(2018, 1, 1))
    def test_list_bill_filter_by_period(self, now_mock):
        response = self.client.get(
            '/bill/',
            {
                'subscriber': '99988526423',
                'period_year': 2016,
                'period_month': 2
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.json(), [
            {
                'id': 1,
                'start_date': '2016-02-29',
                'start_time': '12:00:00',
                'duration': '02:00:00',
                'price': '11.16'
            }
        ])

    @patch('pendulum.now', return_value=pendulum.datetime(2018, 4, 1))
    def test_list_bill_is_returned_by_the_end_record(self, now_mock):
        response = self.client.get(
            '/bill/',
            {
                'subscriber': '99988526423',
                'period_year': 2018,
                'period_month': 3
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.json(), [
            {
                'id': 8,
                'start_date': '2018-02-28',
                'start_time': '21:57:13',
                'duration': '1 00:13:43',
                'price': '86.94'
            }
        ])

    @patch('pendulum.now', return_value=pendulum.datetime(2018, 4, 1))
    def test_list_bill_is_not_returned_by_the_start_record(self, now_mock):
        response = self.client.get(
            '/bill/',
            {
                'subscriber': '99988526423',
                'period_year': 2018,
                'period_month': 2
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.json(), [])

    @patch('pendulum.now', return_value=pendulum.datetime(2017, 1, 1))
    def test_list_bill_filter_by_period_inexistent(self, now_mock):
        response = self.client.get(
            '/bill/',
            {
                'subscriber': '99988526423',
                'period_year': 2019,
                'period_month': 1
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.json(), [])

    @patch('pendulum.now', return_value=pendulum.datetime(2015, 1, 1))
    def test_list_bill_without_previous_period(self, now_mock):
        response = self.client.get(
            '/bill/',
            {
                'subscriber': '99988526423'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.json(), [])

    @patch('pendulum.now', return_value=pendulum.datetime(2019, 1, 1))
    def test_list_bill_filter_subscriber_inexistent(self, now_mock):
        response = self.client.get(
            '/bill/',
            {
                'subscriber': '9999'
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.json(), [])

    @patch('pendulum.now', return_value=pendulum.datetime(2018, 3, 1))
    def test_list_bill_filter_bill_not_closed(self, now_mock):
        response = self.client.get(
            '/bill/',
            {
                'subscriber': '99988526423',
                'period_year': 2018,
                'period_month': 3
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertListEqual(response.json(), [])

    @patch('pendulum.now', return_value=pendulum.datetime(2018, 1, 1))
    def test_list_bill_filter_by_period_without_year(self, now_mock):
        response = self.client.get(
            '/bill/',
            {
                'subscriber': '99988526423',
                'period_month': 2
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'period_year': ['Ensure that this field is filled.']
        })

    @patch('pendulum.now', return_value=pendulum.datetime(2018, 1, 1))
    def test_list_bill_filter_by_period_without_month(self, now_mock):
        response = self.client.get(
            '/bill/',
            {
                'subscriber': '99988526423',
                'period_year': 2019
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertDictEqual(response.json(), {
            'period_month': ['Ensure that this field is filled.']
        })
