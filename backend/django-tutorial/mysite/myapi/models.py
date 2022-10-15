# models.py
from unittest.util import _MAX_LENGTH
from django.db import models

class Transcription(models.Model):
    url = models.CharField(max_length=150)
    language = models.CharField(max_length=20)
    title = models.CharField(max_length=60)
    main_text = models.TextField(blank=True)
    def __str__(self):
        return self.title

    #This subclass (?) forces not to store two of the same pair of url and language
    #This is an alternative to composed primmary key which is not supported for some reason
    #For example you can have one {'url1','spanish'} field with {'url1','english'}
    #but you cant store two {'url1','spanish'}
    class Meta:
        unique_together = ('url', 'language',)
