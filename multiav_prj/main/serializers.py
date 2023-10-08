from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions
from .models import UploadedFile
from .models import ScanResult
from .models import AntivirusEngine
from .models import UserActivityLog


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token





class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'is_staff', 'groups')
        extra_kwargs = {
            "password": {"write_only": True},
        }



class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('id', 'user', 'file', 'uploaded_at')




class ScanResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScanResult
        fields = ('id', 'file', 'scan_status', 'antivirus_engine', 'scan_timestamp')



class AntivirusEngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AntivirusEngine
        fields = ('id', 'name', 'version')




class UserActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivityLog
        fields = ('id', 'user', 'activity_type', 'timestamp')
