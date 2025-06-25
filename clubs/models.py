from django.db import models
from django.contrib.auth.models import User

class Club(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Announcement(models.Model):
    club = models.ForeignKey('Club', on_delete=models.CASCADE, related_name='announcements')
    title = models.CharField(max_length=200)
    body = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.club.name}"

class Member(models.Model):
    club = models.ForeignKey(
        'Club', 
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=100)
    joined_date = models.DateField(auto_now_add=True)
    student_class = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
