# -*- coding: utf-8 -*-
from rest_framework import routers
from .api import CallRecordViewSet

router = routers.SimpleRouter()
router.register(r'call-record', CallRecordViewSet)
urlpatterns = router.urls
