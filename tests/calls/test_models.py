# -*- coding: utf-8 -*-
from decimal import Decimal

import pendulum
from django.test import TransactionTestCase

from olist.calls.models import Bill
from tests.factories import CallRecordStartFactory, CallRecordEndFactory


class BillModelTestCase(TransactionTestCase):
    reset_sequences = True

    def test_calculate_price_without_duration(self):
        start_timestamp = pendulum.datetime(2018, 1, 1)
        end_timestamp = pendulum.datetime(2018, 1, 1)

        CallRecordStartFactory.create(timestamp=start_timestamp)
        CallRecordEndFactory.create(timestamp=end_timestamp)

        bill = Bill.objects.first()

        self.assertEqual(bill.price, Decimal('0.0'))

    def test_calculate_price_on_reduced_hours(self):
        start_timestamp = pendulum.datetime(2018, 1, 1, 22)
        end_timestamp = pendulum.datetime(2018, 1, 1, 22, 4)

        CallRecordStartFactory.create(timestamp=start_timestamp)
        CallRecordEndFactory.create(timestamp=end_timestamp)

        bill = Bill.objects.first()

        self.assertEqual(bill.price, Decimal('0.36'))

    def test_calculate_price_on_standard_hours(self):
        start_timestamp = pendulum.datetime(2018, 1, 1, 15)
        end_timestamp = pendulum.datetime(2018, 1, 1, 15, 4)

        CallRecordStartFactory.create(timestamp=start_timestamp)
        CallRecordEndFactory.create(timestamp=end_timestamp)

        bill = Bill.objects.first()

        self.assertEqual(bill.price, Decimal('0.72'))

    def test_calculate_price_on_standard_hours_and_reduced_hours(self):
        start_timestamp = pendulum.datetime(2018, 1, 1, 0)
        end_timestamp = pendulum.datetime(2018, 1, 2, 0)

        CallRecordStartFactory.create(timestamp=start_timestamp)
        CallRecordEndFactory.create(timestamp=end_timestamp)

        bill = Bill.objects.first()

        self.assertEqual(bill.price, Decimal('86.76'))

    def test_calculate_price_on_reduced_hours_min_edge(self):
        start_timestamp = pendulum.datetime(2018, 1, 1, 21, 59)
        end_timestamp = pendulum.datetime(2018, 1, 1, 22)

        CallRecordStartFactory.create(timestamp=start_timestamp)
        CallRecordEndFactory.create(timestamp=end_timestamp)

        bill = Bill.objects.first()

        self.assertEqual(bill.price, Decimal('0.36'))

    def test_calculate_price_on_reduced_hours_max_edge(self):
        start_timestamp = pendulum.datetime(2018, 1, 1, 5, 59)
        end_timestamp = pendulum.datetime(2018, 1, 1, 6)

        CallRecordStartFactory.create(timestamp=start_timestamp)
        CallRecordEndFactory.create(timestamp=end_timestamp)

        bill = Bill.objects.first()

        self.assertEqual(bill.price, Decimal('0.45'))

    def test_calculate_price_on_fractioned_time(self):
        start_timestamp = pendulum.datetime(2018, 1, 1, 8, 33, 51)
        end_timestamp = pendulum.datetime(2018, 1, 1, 8, 35, 45)

        CallRecordStartFactory.create(timestamp=start_timestamp)
        CallRecordEndFactory.create(timestamp=end_timestamp)

        bill = Bill.objects.first()

        self.assertEqual(bill.price, Decimal('0.45'))

    def test_calculate_price_on_fractioned_time_without_complete_cycle(self):
        start_timestamp = pendulum.datetime(2018, 1, 1, 8, 33, 1)
        end_timestamp = pendulum.datetime(2018, 1, 1, 8, 33, 58)

        CallRecordStartFactory.create(timestamp=start_timestamp)
        CallRecordEndFactory.create(timestamp=end_timestamp)

        bill = Bill.objects.first()

        self.assertEqual(bill.price, Decimal('0.0'))
