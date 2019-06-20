# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework.documentation import include_docs_urls


API_TITLE = 'Olist Calls Documentation'
API_DESCRIPTION = """
    Olist Calls is an application that helps in tracking the calls that your company makes.
    Through it, it's possible to monitor and audit in real time all the data necessary for good management.
    The relevant data reports allow you to take care of your business in a much simpler way.
"""

urlpatterns = [
    path(r'', include('olist.calls.urls')),
    path(r'docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION))
]
