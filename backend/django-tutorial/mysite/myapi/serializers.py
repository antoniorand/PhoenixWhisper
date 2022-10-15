# 1. Import the Hero model
# 2. Import the REST Framework serializer
# 3. Create a new class that links the Hero with its serializer

# serializers.py
from rest_framework import serializers

from .models import Transcription

class TranscriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Transcription
        fields = ('id','url', 'title','main_text','language')

