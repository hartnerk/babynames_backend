from rest_framework import viewsets
from django.contrib.auth.models import User
from .models import UserPreferences, UserCouples, UserNamePools, BabyNames, LikedNames
from . serializers import UserSerializer, UserPreferencesSerializer, UserCouplesSerializer, UserNamePoolsSerializer, BabyNamesSerializer, LikedNamesSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserPreferencesViewSet(viewsets.ModelViewSet):
    queryset = UserPreferences.objects.all()
    serializer_class = UserPreferencesSerializer


class UserCoupleViewSet(viewsets.ModelViewSet):
    queryset = UserCouples.objects.all()
    serializer_class = UserCouplesSerializer


class UserNamesPoolViewSet(viewsets.ModelViewSet):
    queryset = UserNamePools.objects.all()
    serializer_class = UserNamePoolsSerializer


class BabyNameViewSet(viewsets.ModelViewSet):
    queryset = BabyNames.objects.all()
    serializer_class = BabyNamesSerializer


# class BabyNameViewSet(viewsets.ModelViewSet):
#     queryset = BabyName.objects.all()
#     serializer_class = BabyNameSerializer


class LikedNameViewSet(viewsets.ModelViewSet):
    queryset = LikedNames.objects.all()
    serializer_class = LikedNamesSerializer
