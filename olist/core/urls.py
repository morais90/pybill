# -*- coding: utf-8 -*-
from django.urls import path, include


urlpatterns = [
    path(r'', include('olist.calls.urls'))
]
