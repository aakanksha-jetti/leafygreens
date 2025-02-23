from django.db import models

class veggies(models.Model):
    id = models.AutoField(primary_key=True) 
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    stock= models.IntegerField()
    img =models.ImageField(upload_to='pics')
    desc=models.TextField()
    def __str__(self): # Add this for better representation
        return self.name


# Create your models here.

