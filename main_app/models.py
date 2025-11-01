from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth import get_user_model
from phonenumber_field.phonenumber import PhoneNumber
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models import UniqueConstraint
# Create your models here.

User = get_user_model()

# Add more fields to your user
class Skill (models.Model):
    type= models.CharField (max_length=100)
    name= models.CharField (max_length=100)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['type', 'name'], 
                name='unique_skill')
            ]
        
    def __str__(self):
        return self.name

class Meeting (models.Model):
    date= models.DateField ('Meeting data')
    time= models.TimeField ('Meeting data')
    is_complete= models.BooleanField ()
    rate= models.PositiveIntegerField (validators= [MaxValueValidator(5)], blank=True, null=True)

    def __str__(self):
        return f'Metting on:{self.date } - {self.time}'

class UserProfile(models.Model):
    birth_date = models.DateField()
    level = models.CharField()
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills =  models.ManyToManyField(Skill, through='UserSkill', blank=True)
    # meetings =  models.ForeignKey(Meeting, blank=True)

    def __str__(self):
        return self.user.username

class UserSkill (models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill,on_delete=models.CASCADE )
    role = models.CharField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'skill', 'role'], 
                name='unique_user_skill')
            ]
        
    def __str__(self):
        return f'{self.user} - {self.role} - {self.skill}'

    

class Experience (models.Model):
    date= models.DateField ('Experience data')
    title = models.CharField (max_length=100)
    description= models.CharField (max_length=100)
    place= models.CharField (max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title



class Certificate (models.Model):
    type= models.CharField (max_length=100)
    name= models.CharField (max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name