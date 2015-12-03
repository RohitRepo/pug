from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect

from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied

from .models import Device
from .serializers import DeviceSerializer
from accounts.models import User
from broker.api import turn_device_on, turn_device_off


@permission_classes((permissions.AllowAny,))
@api_view(['POST'])
def add_device(request, format=None):
    serializer = DeviceSerializer(data=request.data)
    if serializer.is_valid():
        user_token = serializer.validated_data['user_token']
        user = get_object_or_404(User, email=user_token)
        device = serializer.save(owner=user)
        return Response({'id': device.id}, status=status.HTTP_201_CREATED)

    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes((permissions.IsAuthenticated,))
@api_view(['GET'])
def user_devices(request, format=None):
    devices = request.user.devices.all()
    serializer = DeviceSerializer(devices, many=True)
    return Response(serializer.data)

@permission_classes((permissions.IsAuthenticated,))
@api_view(['POST'])
def device_on(request, device_id):
    device = get_object_or_404(Device, id=device_id)

    if device.owner.id != request.user.id:
        raise PermissionDenied

    try:
        result = turn_device_on(device.id)

        if result:
            return Response()
        return Response(status.HTTP_503_SERVICE_UNAVAILABLE)
    except:
        return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes((permissions.IsAuthenticated,))
@api_view(['POST'])
def device_off(request, device_id):
    device = get_object_or_404(Device, id=device_id)

    if device.owner.id != request.user.id:
        raise PermissionDenied

    try:
        result = turn_device_off(device.id)

        if result:
            return Response()
        return Response(status.HTTP_503_SERVICE_UNAVAILABLE)
    except:
        return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)