from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class task(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=50, choices=[
        ('Pending','Pending'),
        ('Done','Done'),
    ], default="Pending")

    def __str__(self):
        return self.title
    