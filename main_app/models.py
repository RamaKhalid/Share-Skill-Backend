from django.db import models

# Create your models here.
#
class Skill (models.Model):
    type= models.CharField (max_length=100)
    name= models.CharField (max_length=100)

    def __str__(self):
        return self.name
    

class Experience (models.Model):
    date= models.DateField ('Experience data')
    description= models.CharField (max_length=100)
    place= models.CharField (max_length=100)