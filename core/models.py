from re import S
from django.db import models


class Criteria(models.Model):
    name = models.CharField(max_length=100)
    mark = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class SubCriteria(models.Model):
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    mark = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Observation(models.Model):
    message = models.CharField(max_length=300)

    def __str__(self):
        return self.message


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
    observations = models.ManyToManyField(Observation)

    def __str__(self):
        return self.name


class SoldierMark(models.Model):
    soldier = models.ForeignKey(Soldier, on_delete=models.CASCADE)
    sub_criteria = models.ForeignKey(SubCriteria, on_delete=models.CASCADE)
    mark = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.sub_criteria.name + ": " + str(self.mark)