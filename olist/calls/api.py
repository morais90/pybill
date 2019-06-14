# -*- coding: utf-8 -*-
from rest_framework import viewsets

from .models import CallRecord
from .serializers import CallRecordStartSerializer, CallRecordEndSerializer


class CallRecordViewSet(viewsets.ModelViewSet):
    queryset = CallRecord.objects.all()

    def get_serializer_class(self):
        data = self.request.data

        if data.get('type') == CallRecord.START_RECORD:
            return CallRecordStartSerializer
        return CallRecordEndSerializer
