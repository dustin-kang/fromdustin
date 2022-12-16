from django.db import models
from django.contrib.auth.models import User
import os

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    
    head_image = models.ImageField(upload_to='blogs/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blogs/files/%Y/%m/%d/', blank=True)

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'
    