# -*- coding: utf-8 -*-
from django.test import TransactionTestCase

from olist.calls.models import Bill
from tests.factories import CallRecordStartFactory, CallRecordEndFactory


class CallRecordPostSaveTestCase(TransactionTestCase):
    reset_sequences = True

    def test_post_save_does_not_create_bill_without_end_pair(self):
        CallRecordStartFactory.create()

        self.assertEqual(Bill.objects.count(), 0)

    def test_post_save_does_not_create_bill_without_start_pair(self):
        CallRecordEndFactory.create()

        self.assertEqual(Bill.objects.count(), 0)

    def test_post_save_create_bill_on_start_pair_founded(self):
        end_record = CallRecordEndFactory.create()
        start_record = CallRecordStartFactory.create()

        self.assertTrue(Bill.objects.filter(start_record=start_record, end_record=end_record).exists())

    def test_post_save_create_bill_on_end_pair_founded(self):
        start_record = CallRecordStartFactory.create()
        end_record = CallRecordEndFactory.create()

        self.assertTrue(Bill.objects.filter(start_record=start_record, end_record=end_record).exists())
