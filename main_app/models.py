from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
#
class Skill (models.Model):
    type= models.CharField (max_length=100)
    name= models.CharField (max_length=100)

    def __str__(self):
        return self.name
    

class Experience (models.Model):
    date= models.DateField ('Experience data')
    title = models.CharField (max_length=100)
    description= models.CharField (max_length=100)
    place= models.CharField (max_length=100)


class Meeting (models.Model):
    date= models.DateField ('Meeting data')
    time= models.TimeField ('Meeting data')
    is_complete= models.BooleanField ()
    rate= models.PositiveIntegerField (validators= [MaxValueValidator(5)])

    def __str__(self):
        return f'Metting on:{self.date } - {self.time}'

class Certificate (models.Model):
    type= models.CharField (max_length=100)
    name= models.CharField (max_length=100)

    def __str__(self):
        return self.name