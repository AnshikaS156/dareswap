from django.db import models

# Create your models here.
class DareExchange(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=254, null= True, blank=True)
    DareTitle = models.CharField(max_length=100)
    Description = models.CharField(max_length=100, null=True, blank=True)
    Difficulty = models.CharField(max_length=10, null=True, blank=True)
    Category = models.CharField(max_length=100, null=True, blank=True)
    Deadline= models.DateField(blank=True, null=True)
    Tags = models.CharField(max_length=100, null=True, blank=True)
    dare_image=models.ImageField(upload_to="dare_images/",blank=True, null= True)
    is_edited = models.BooleanField(default =False)
    # def __str__(self):
    #     return self.DareTitle