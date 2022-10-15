# 1. Query the database for all heroes
# 2. Pass that database queryset into the serializer we just created, so that it gets converted into JSON and rendered

from rest_framework import viewsets

from .serializers import TranscriptionSerializer
from .models import Transcription


class TranscriptionViewSet(viewsets.ModelViewSet):
    queryset = Transcription.objects.all().order_by('title')
    serializer_class = TranscriptionSerializer