# 1. Query the database for all heroes
# 2. Pass that database queryset into the serializer we just created, so that it gets converted into JSON and rendered

from rest_framework import viewsets

from .serializers import YTSerializer
from .models import Youtube


class YTViewSet(viewsets.ModelViewSet):
    queryset = Youtube.objects.all().order_by('id')
    serializer_class = YTSerializer