from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name