from django.db import models
from django.contrib.auth.models import User


class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class ScanResult(models.Model):
    file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    scan_status = models.CharField(max_length=20)  # Clean, Infected, etc.
    antivirus_engine = models.CharField(max_length=50)
    scan_timestamp = models.DateTimeField(auto_now_add=True)
    # Other fields to store additional scan-related information


class AntivirusEngine(models.Model):
    name = models.CharField(max_length=100)
    version = models.CharField(max_length=20)
    # Other fields for engine configuration, API endpoints, etc.



class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)  # Login, File Upload, Scan, etc.
    timestamp = models.DateTimeField(auto_now_add=True)
    # Other fields for additional log information
