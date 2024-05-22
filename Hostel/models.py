from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.conf import settings


# Create your models here.
# models.py in your app

class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Gender(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Level (models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    

class CustomUser(AbstractUser):
    matric_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    faculty = models.ForeignKey('Faculty', on_delete=models.SET_NULL, null=True)
    gender = models.ForeignKey('Gender', on_delete=models.SET_NULL, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    hostel = models.ForeignKey('Hostel', on_delete=models.SET_NULL, null=True)
    block = models.ForeignKey('Block', on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True)
    bunk = models.ForeignKey('Bunk', on_delete=models.SET_NULL, null=True)
    space = models.ForeignKey('BedSpace', on_delete=models.SET_NULL, null=True)
    level = models.ForeignKey('Level', on_delete=models.SET_NULL, null=True)
    has_paid_hostel_fee = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Hostel(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    # Add any other relevant fields

    def __str__(self):
        return self.name

class Block(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    # Add any other relevant fields

    def __str__(self):
        return f"{self.hostel} - {self.name}"

class Room(models.Model):
    block = models.ForeignKey(Block, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=10, default=1)
    # Add any other relevant fields

    def __str__(self):
        return f"{self.block} - {self.name}"

class Bunk(models.Model):
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    name = models. CharField(max_length=10)
    # position = models.CharField(max_length=50)  # 'Up' or 'Down'
    # Add any other relevant fields

    def __str__(self):
        return f"{self.room} - {self.name}"

class BedSpace(models.Model):
    bunk = models.ForeignKey(Bunk, on_delete=models.SET_NULL, null=True, default='1')
    position = models.CharField(max_length=4, choices=[('Up', 'Up'), ('Down', 'Down')])
    is_allocated= models.BooleanField(default=False)
    class Meta:
        unique_together = ('bunk', 'position')
    def __str__(self):
        return f"{self.bunk} - {self.position}"

class Complaint (models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    title = models.CharField(max_length = 100)
    block_number = models.CharField(max_length = 100)
    room_number = models.CharField(max_length = 100)
    message = models.TextField()
    image = models.ImageField(upload_to='complaints_image')
    hostel_name = models.CharField(max_length=100, default='male new hostel')

    def __str__(self):
        return f"{self.title} - Room {self.room_number} in Block {self.block_number}"
    
CHOICE_FOR_EXEAT = (
    ("PENDING", 'Exeact request is pending'),
    ("APPROVED", 'Approved by admin'),
    ("REJECTED", 'Rejected by Admin')
)
class Exeat(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent_number = models.CharField(max_length=11)
    departure_date = models.DateField()
    return_date = models.DateField()
    reason = models.TextField()
    department = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    level = models.CharField(max_length=10)
    student_number = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=CHOICE_FOR_EXEAT, default=CHOICE_FOR_EXEAT[0][0])
    
    def __str__(self):
        return f"{self.user} - {self.departure_date} to {self.return_date}"


@receiver(pre_save, sender=Exeat)
def exeact_pre_save(sender, instance, **kwargs):
    # Check if the save is being triggered from the admin panel
    if hasattr(instance, '_state') and hasattr(instance._state, 'adding') and not instance._state.adding:
        # pre-save logic
        from .views import send_mail
        if instance.status == "APPROVED" or instance.status == "REJECTED":
            send_mail(instance)


class Upload(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    evidence = models.ImageField(upload_to = 'evidence-of-payment')
    created = models.DateTimeField(auto_now_add = True)
    
    def __str__ (self):
        return  f"{self.user} - {self.evidence}"


class Amount(models.Model):
    price = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.price

class Payment(models.Model):
    matric_number = models.CharField(max_length = 15)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.matric_number


class Paid(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField()

    def __str__(self):
        return self.email