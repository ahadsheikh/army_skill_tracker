from django.db import models
from django.contrib.auth.models import User

USER_TYPE_CHOICES = (
    ('A', 'Admin'),
    ('C', 'Clerk'),
    ('S', 'Soldier'),
)


class Clerk(models.Model):
    """
    Clerk model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    personal_no = models.PositiveBigIntegerField(unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    rank = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    unit = models.CharField(max_length=20)
    subunit = models.CharField(max_length=20)
    starting_date = models.DateField(auto_now_add=True)
    contact = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to='profile_pics', default="army.jpg" ,blank=True)

    def __str__(self):
        return self.name