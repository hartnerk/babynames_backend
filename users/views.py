from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import UserPreferences, UserCouples, UserNamePools, BabyNames, LikedNames
from rest_framework.views import APIView
from . serializers import NewUserSerializer, UserSerializer, UserPreferencesSerializer, UserCouplesSerializer, UserNamePoolsSerializer, BabyNamesSerializer, LikedNamesSerializer

import sqlite3 


@api_view(['GET'])
def get_names_from_prefs(request):
    
    side1 = request.user.couple_user_one.first()
    side2 = request.user.couple_user_two.first()

    if side1:
        couple = side1
        query = BabyNames.objects.filter(gender=couple.preferences.gender, usage=couple.preferences.origin)
        serializer = BabyNamesSerializer(query, many=True)

    elif side2:
        couple = side2
        query = BabyNames.objects.filter(gender=couple.preferences.gender, usage=couple.preferences.origin)
        serializer = BabyNamesSerializer(query, many=True)

    else:
        serializer = BabyNamesSerializer(BabyNames.objects.none(), many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)



class NewUser(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format='json'):
        # print(request)
        serializer = NewUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserPreferencesViewSet(viewsets.ModelViewSet):
    queryset = UserPreferences.objects.all()
    serializer_class = UserPreferencesSerializer


class UserCouplesViewSet(viewsets.ModelViewSet):
    queryset = UserCouples.objects.all()
    serializer_class = UserCouplesSerializer


class UserNamePoolsViewSet(viewsets.ModelViewSet):
    queryset = UserNamePools.objects.all()
    serializer_class = UserNamePoolsSerializer


class BabyNamesViewSet(viewsets.ModelViewSet):
    queryset = BabyNames.objects.all()
    serializer_class = BabyNamesSerializer


class LikedNamesViewSet(viewsets.ModelViewSet):
    queryset = LikedNames.objects.all()
    serializer_class = LikedNamesSerializer
