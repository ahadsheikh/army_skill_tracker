from django.db import models


class Soldier(models.Model):
    personal_no = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=100)
    rank = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    subunit = models.CharField(max_length=20)
    appointment = models.CharField(max_length=50)
    join_date = models.DateField(blank=True)
    commision_date = models.DateField(blank=True)
    contact = models.CharField(max_length=50)
    previous_company = models.CharField(max_length=20)
    mission = models.CharField(max_length=45)

    def __str__(self):
        return self.name


