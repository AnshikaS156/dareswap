from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    GENDER_CHOICES = (
                      
        ("Male","Male"),
        ("Female","Female"),
        ("Other","Other"),
        
    )
 
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)

class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"