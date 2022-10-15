# models.py
from unittest.util import _MAX_LENGTH
from django.db import models

class Youtube(models.Model):
    URL = models.CharField(max_length=60)
    def __str__(self):
        return self.URL

