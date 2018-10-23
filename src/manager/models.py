from django.db import models#do not understand only key

class TestData(models.Model):
    info_id = models.IntegerField()
    info = models.CharField(max_length=50)