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
def set_couple(request):
    if request.method=='POST':
        print('in SET USER')
        return JsonResponse({}, status=status.HTTP_200_OK)
    #     data = json.load(request)  
    #     print('in SET USER', data)
    #     # form = AlertForm(data)
    #     # if form.is_valid():
    #     #     alert_form = form.save(commit=False)
    #     #     form.save()
    #     #     new_data = json.loads(serialize('json', [alert_form]))
    #     #     return JsonResponse(data=new_data, status=200, safe=False)
    
    # user1 = User.objects.filter(id=request.user.id)
    # user1 = UserSerializer(user1)
    # user2 = User.objects.filter(username=data['partnerName'])
    # user2 = UserSerializer(user2)   
    # return Response(serializer.data, status=status.HTTP_200_OK)
