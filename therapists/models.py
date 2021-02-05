from django.db import models


class Therapist(models.Model):
    therapist_id = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=60)
    methods = models.TextField(max_length=300)
    photo_id = models.CharField(max_length=300, blank=True)
    photo_link = models.URLField()
    created_time = models.CharField(max_length=100, blank=True)


class RawData(models.Model):
    date = models.DateField()
    raw_data = models.TextField()
