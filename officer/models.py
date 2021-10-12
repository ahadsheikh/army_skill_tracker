from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import datetime


class Officer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ba_no = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    rank = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    subunit = models.CharField(max_length=20)
    appointment = models.CharField(max_length=50)
    starting_date = models.DateField(auto_now_add=True)
    ending_date = models.DateField(null=True, blank=True)
    contact = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to='profile_pics/officers', default="army.jpg" ,blank=True)

    def __str__(self):
        return self.name

    def end_officer_duty(self):
        self.ending_date = datetime.today()
        self.save()