# -*- coding: utf-8 -*-
from rest_framework import routers
from .api import CallRecordViewSet, BillViewSet


router = routers.SimpleRouter()
router.register(r'call-record', CallRecordViewSet)
router.register(r'bill', BillViewSet, base_name='bill')
urlpatterns = router.urls
