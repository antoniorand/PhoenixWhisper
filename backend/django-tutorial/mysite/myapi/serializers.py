# 1. Import the Hero model
# 2. Import the REST Framework serializer
# 3. Create a new class that links the Hero with its serializer

# serializers.py
from rest_framework import serializers

from .models import Youtube

class YTSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Youtube
        fields = ('id', 'URL')

