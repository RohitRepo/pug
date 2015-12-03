from .models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect

@api_view(['POST'])
def login_user(request, format=None):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = User.objects.get(email=email)
        user = authenticate(username=email, password=password)
        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if user.is_active:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_402_PAYMENT_REQUIRED)
    except User.DoesNotExist:
        return Response(status=status.HTTP_409_CONFLICT)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def logout_user(request, format=None):
    logout(request)
    next_url = request.GET.get('next', '/')
    return redirect(next_url)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_current_user(request, format=None):
    if request.user.is_authenticated():
        return Response(ExistingUserSerializer(request.user, context={'request': request}).data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

