from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Content(models.Model):
    CONTENT_TYPES = (
        ('ویدیو', 'ویدیو'),
        ('عکس', 'عکس'),
        ('متن', 'متن'),
    )
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES)
    file = models.FileField(upload_to='content/')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PublishReport(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    instagram_success = models.BooleanField(default=False)
    instagram_error = models.TextField(null=True, blank=True)
    telegram_success = models.BooleanField(default=False)
    telegram_error = models.TextField(null=True, blank=True)
    facebook_success = models.BooleanField(default=False)
    facebook_error = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"گزارش برای {self.content.title} - {self.created_at}"