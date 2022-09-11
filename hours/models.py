from django.db import models
from django.utils import timezone


class ResourceStatus(models.Model):
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.status


class HrsAppResource(models.Model):
    name = models.CharField(max_length=200)
    status = models.ForeignKey(ResourceStatus, on_delete=models.CASCADE)
    url = models.URLField(max_length=500, blank=True, null=True)
    recent_date = models.DateField('recent date', blank=True, null=True)

    def __str__(self):
        return self.name


class HrsAppDataType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class HrsAppParameter(models.Model):
    name = models.CharField(max_length=200)
    data_type = models.ForeignKey(HrsAppDataType, on_delete=models.CASCADE)
    string_value = models.CharField(max_length=200, blank=True, null=True)
    integer_value = models.BigIntegerField(blank=True, null=True)
    float_value = models.FloatField(blank=True, null=True)
    datetime_value = models.DateTimeField('datetime value', blank=True, null=True)

    def __str__(self):
        return self.name
