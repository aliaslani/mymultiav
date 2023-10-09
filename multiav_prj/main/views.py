from rest_framework import viewsets
from rest_framework import permissions
from hashlib import md5
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from rest_framework.throttling import UserRateThrottle
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import MyTokenObtainPairSerializer, UserSerializer
import docker
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class MyTokenObtainPairSerializer(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    throttle_classes = [UserRateThrottle]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # if 'password' in request.data:
        #     request.data['password'] = instance.set_password(request.data['password'])
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if 'password' in request.data:
            instance.set_password(request.data['password'])
            instance.save()
        self.perform_update(serializer)
        return Response(serializer.data)




class ScanFileView(APIView):
    queryset = User.objects.all()
    def post(self, request, format=None):
        # Get the uploaded file from the request
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create a Docker client
            client = docker.from_env()

            # Run the antivirus engine container, passing the file to scan
            container = client.containers.run(
                image='clamav/clamav:latest',
                command=['clamscan', '-'],
                stdin_open=True,
                tty=False,
                detach=True,
            )

            try:
                # Write the file to the container's STDIN for scanning
                container.exec_run(
                    cmd=['bash', '-c', f'echo "{uploaded_file.read().decode()}" | clamscan -'],
                    stdout=True,
                    stderr=True,
                )

                # Wait for the container to finish scanning
                container.wait()

                # Get the container's exit code to determine the scan result
                exit_code = container.attrs['State']['ExitCode']

                # Handle the scan result based on the exit code
                result = 'Clean' if exit_code == 0 else 'Infected'
            finally:
                # Stop the container
                container.stop()

            # Remove the container after it has been stopped
            container.remove()

            return Response({'result': result}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)