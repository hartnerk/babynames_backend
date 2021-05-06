from rest_framework import viewsets, permissions, status
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserPreferences, UserCouples, UserNamePools, BabyNames, LikedNames, User
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.views import APIView
import json
from django.http import JsonResponse
from . serializers import NewUserSerializer, UserSerializer, UserPreferencesSerializer, UserCouplesSerializer, UserNamePoolsSerializer, BabyNamesSerializer, LikedNamesSerializer

class NewUser(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format='json'):
        serializer = NewUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format='json'):
        serializer = NewUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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


# class BabyNameViewSet(viewsets.ModelViewSet):
#     queryset = BabyName.objects.all()
#     serializer_class = BabyNameSerializer


class LikedNamesViewSet(viewsets.ModelViewSet):
    queryset = LikedNames.objects.all()
    serializer_class = LikedNamesSerializer

@csrf_exempt
@api_view(['POST'])
def set_couple(request):
    user2 = User.objects.get(username=request.data['partnerUserame'])        
    couple = UserCouples.objects.create(user_one=request.user, user_two=user2)
    couple.save()
    serializer = UserCouplesSerializer(couple)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['POST'])
def set_preferences(request):
    if request.user.couple_user_one.first():
         usercouple_id = request.user.couple_user_one.first()
    elif request.user.couple_user_two.first():
        usercouple_id = request.user.couple_user_two.first()
    else:
        usercouple_id =''
    gender = request.data['gender']
    origin = request.data['origin']
    couplePreferences = UserPreferences.objects.create(usercouple_id=usercouple_id, gender=gender, origin=origin)
    couplePreferences.save()
    serializer=UserPreferencesSerializer(couplePreferences)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)