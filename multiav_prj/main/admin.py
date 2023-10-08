from django.contrib import admin
from .models import User, UploadedFile, ScanResult, AntivirusEngine, UserActivityLog


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'file', 'uploaded_at']

@admin.register(ScanResult)
class ScanResultAdmin(admin.ModelAdmin):
    list_display = ['id', 'file', 'scan_status', 'antivirus_engine', 'scan_timestamp']

@admin.register(AntivirusEngine)
class AntivirusEngineAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'version']

@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'activity_type', 'timestamp']

