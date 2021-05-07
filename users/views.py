from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserPreferences, UserCouples, UserNamePools, BabyNames, LikedNames, User, UserLikedNames
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.views import APIView
import json
from django.http import JsonResponse
from . serializers import NewUserSerializer, UserSerializer, UserPreferencesSerializer, UserCouplesSerializer, UserNamePoolsSerializer, BabyNamesSerializer, LikedNamesSerializer, UserLikedNamesSerializer
from . serializers import NewUserSerializer, UserSerializer, UserPreferencesSerializer, UserCouplesSerializer, UserNamePoolsSerializer, BabyNamesSerializer, LikedNamesSerializer;
from rest_framework_extensions.mixins import NestedViewSetMixin
from django.db.models import Max

import sqlite3 
import random

@api_view(['GET'])
def get_user_info(request):
    # breakpoint()
    if request.user.couple_user_one.first():
         usercouple_id = request.user.couple_user_one.first()
    elif request.user.couple_user_two.first():
        usercouple_id = request.user.couple_user_two.first()
    else:
        usercouple_id = ''

    userdata = {'user_id': f'{request.user.id}',
                'username': f'{request.user.username}'}

    if not usercouple_id == '':          
        serializer=UserCouplesSerializer(usercouple_id)
        userdata.update(serializer.data)
    #breakpoint()
    return Response(userdata, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_names_from_prefs(request):

    side1 = request.user.couple_user_one.first()
    side2 = request.user.couple_user_two.first()

    # breakpoint()

    if side1:
        couple = side1
        if couple.preferences.gender == '' and couple.preferences.origin == '':
            query = BabyNames.objects.all()
        elif couple.preferences.gender == '':
            query = BabyNames.objects.filter(usage=couple.preferences.origin)
        elif couple.preferences.origin == '':
            query = BabyNames.objects.filter(gender=couple.preferences.gender.lower())
        else:
            query = BabyNames.objects.filter(gender=couple.preferences.gender.lower(), usage=couple.preferences.origin)
        serializer = BabyNamesSerializer(query, many=True)

    elif side2:
        couple = side2
        if couple.preferences.gender == '' and couple.preferences.origin == '':
            query = BabyNames.objects.all()
        elif couple.preferences.gender == '':
            query = BabyNames.objects.filter(usage=couple.preferences.origin)
        elif couple.preferences.origin == '':
            query = BabyNames.objects.filter(gender=couple.preferences.gender.lower())
        else:
            query = BabyNames.objects.filter(gender=couple.preferences.gender.lower(), usage=couple.preferences.origin)
        serializer = BabyNamesSerializer(query, many=True)

    else:
        query = BabyNames.objects.none()
        serializer = BabyNamesSerializer(query, many=True)

    # breakpoint()
    names_list_full = list(query)
    if len(names_list_full) > 100:
        names_list = random.sample(names_list_full, 100)
    else:
        names_list = names_list_full
    # random.shuffle(names_list)
    #breakpoint()
    if not UserNamePools.objects.filter(usercouple_id=couple).exists():
        instance = UserNamePools.objects.create(usercouple_id=couple)
        instance.names.set(names_list)
    else:
        instance = UserNamePools.objects.get(usercouple_id=couple)
        instance.names.set(names_list)
    # breakpoint()
    
    return Response(serializer.data, status=status.HTTP_200_OK)



class NewUser(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format='json'):
        serializer = NewUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format='json'):
        serializer = NewUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserPreferencesViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = UserPreferences.objects.all()
    serializer_class = UserPreferencesSerializer


class UserCouplesViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = UserCouples.objects.all()
    serializer_class = UserCouplesSerializer


class UserNamePoolsViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = UserNamePools.objects.all()
    serializer_class = UserNamePoolsSerializer


class BabyNamesViewSet(viewsets.ModelViewSet):
    queryset = BabyNames.objects.all()
    serializer_class = BabyNamesSerializer

class UserLikedNamesViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = UserLikedNames.objects.all()
    serializer_class = UserLikedNamesSerializer

class LikedNamesViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    serializer_class = LikedNamesSerializer
    queryset = LikedNames.objects.all()
    def get_queryset(self):
        queryset = super().get_queryset()
        matched = self.request.query_params.get('matched')
        if matched is not None:
            queryset = queryset.filter(matched=matched)
        return queryset

@csrf_exempt
@api_view(['POST'])
def set_couple(request):
    user2 = User.objects.get(username=request.data['partnerUsername'])        
    couple = UserCouples.objects.update_or_create(user_one=request.user, defaults={'user_two':user2})[0]
    couple.save()
    serializer = UserCouplesSerializer(couple)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['POST'])
def set_preferences(request):
    #breakpoint()
    if request.user.couple_user_one.first():
         usercouple_id = request.user.couple_user_one.first()
    elif request.user.couple_user_two.first():
        usercouple_id = request.user.couple_user_two.first()
    else:
        usercouple_id =''
    gender = request.data['gender']
    origin = request.data['origin']

    couplePreferences = UserPreferences.objects.update_or_create(usercouple_id=usercouple_id, defaults={'gender': gender, 'origin':origin})[0]
    print(couplePreferences)
    couplePreferences.save()
    serializer=UserPreferencesSerializer(couplePreferences)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    def get_queryset(self):
        queryset = LikedNames.objects.all()
        matched = self.request.query_params.get('matched')
        if matched is not None:
            queryset = queryset.filter(matched=matched)
        return queryset


@csrf_exempt
@api_view(['POST'])
def deletelikedname(request):
    if request.user.couple_user_one.first():
         usercouple_id = request.user.couple_user_one.first()
    elif request.user.couple_user_two.first():
        usercouple_id = request.user.couple_user_two.first()
    else:
        usercouple_id =''
    name = name = request.data['customName']
    BabyNames.objects.filter(baby_name=name).first()
    likename = LikedNames.objects.filter(usercouple_id=usercouple_id, name_id=BabyNames.objects.filter(baby_name=name).first()).first()
    likename.delete()
    nameInPool = UserNamePools.objects.get(usercouple_id=usercouple_id)
    serializer=UserNamePoolsSerializer(nameInPool)

    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

@csrf_exempt
@api_view(['POST'])
def add_my_name(request):
    if request.user.couple_user_one.first():
         usercouple_id = request.user.couple_user_one.first()
    elif request.user.couple_user_two.first():
        usercouple_id = request.user.couple_user_two.first()
    else:
        usercouple_id =''
    name = request.data['customName']
    if(BabyNames.objects.filter(baby_name=name).exists()):
        # breakpoint()
        likename = LikedNames(usercouple_id=usercouple_id, name_id=BabyNames.objects.filter(baby_name=name).first(), matched=False, order=LikedNames.objects.filter(usercouple_id=1).aggregate(Max('order'))['order__max'])
        likename.save()

    else:
        newName = BabyNames.objects.create(baby_name=name, gender=request.data['gender'], usage='user_added')
        newName.save()
        likename = LikedNames(usercouple_id=usercouple_id, name_id=newName, matched=False, order=LikedNames.objects.filter(usercouple_id=1).aggregate(Max('order'))['order__max'])
        likename.save()
    nameInPool, created = UserNamePools.objects.get_or_create(usercouple_id=usercouple_id)
    newpool=nameInPool.names.add(BabyNames.objects.filter(baby_name=name).first().id)
    serializer=UserNamePoolsSerializer(nameInPool)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@csrf_exempt
@api_view(['POST'])
def match_order(request):
    if request.user.couple_user_one.first():
         usercouple_id = request.user.couple_user_one.first()
    elif request.user.couple_user_two.first():
        usercouple_id = request.user.couple_user_two.first()
    else:
        usercouple_id =''
    user1 = UserCouples.objects.filter(id=usercouple_id.id)[0].user_one
    user2 = UserCouples.objects.filter(id=usercouple_id.id)[0].user_two
    if user1.id == request.user.id:
        user2_id = user2.id
    else:
        user2_id = user1.id
    match_query = LikedNames.objects.all().filter(usercouple_id=usercouple_id).filter(matched=True)
    for object in match_query:
        user1Rank = UserLikedNames.objects.filter(user_id=request.user.id).filter(name_id=object.name_id)[0].order
        user2Rank = UserLikedNames.objects.filter(user_id=user2_id).filter(name_id=object.name_id)[0].order
        overallRank = user1Rank + user2Rank
        object.order = overallRank
        object.save()
    return Response({"data":1}, status=status.HTTP_201_CREATED )

