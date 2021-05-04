from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import UserPreferences, UserCouple, UserNamesPool, BabyName, LikedName
from . serializers import UserSerializer, UserPreferencesSerializer, UserCoupleSerializer, UserNamesPoolSerializer, BabyNameSerializer, LikedNameSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserPreferencesViewSet(viewsets.ModelViewSet):
    queryset = UserPreferences.objects.all()
    serializer_class = UserPreferencesSerializer


class UserCoupleViewSet(viewsets.ModelViewSet):
    queryset = UserCouple.objects.all()
    serializer_class = UserCoupleSerializer


class UserNamesPoolViewSet(viewsets.ModelViewSet):
    queryset = UserNamesPool.objects.all()
    serializer_class = UserNamesPoolSerializer


class BabyNameViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = BabyName.objects.all()
    serializer_class = BabyNameSerializer


class BabyNameViewSet(viewsets.ModelViewSet):
    queryset = BabyName.objects.all()
    serializer_class = BabyNameSerializer


class LikedNameViewSet(viewsets.ModelViewSet):
    queryset = LikedName.objects.all()
    serializer_class = LikedNameSerializer
