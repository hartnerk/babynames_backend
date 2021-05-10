from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserPreferences, UserCouples, UserNamePools, BabyNames, LikedNames, User, UserLikedNames, UserDislikedNames
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.views import APIView
import json
from django.http import JsonResponse
from . serializers import NewUserSerializer, UserSerializer, UserPreferencesSerializer, UserCouplesSerializer, UserNamePoolsSerializer, BabyNamesSerializer, LikedNamesSerializer, UserLikedNamesSerializer, UserDislikedNamesSerializer
from rest_framework_extensions.mixins import NestedViewSetMixin
from django.db.models import Max
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse


import sqlite3 
import random

@api_view(['GET'])
def get_user_info(request):
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
    return Response(userdata, status=status.HTTP_200_OK)


@api_view(['GET'])
def recomendations(request):
    datafull=[[0]] 
    users=UserSerializer(User.objects.all(), many=True)
    # likes=UserLikedNamesSerializer(UserLikedNames.objects.all(), many=True)
    # disliked=UserDislikedNamesSerializer(UserDislikedNames.objects.all(), many=True)
    for userindex, user in enumerate(users.data):
        # print('your printing each username: ', user['username'])
        data=[0] * len(datafull[0])
        data[0] = user['id']   #add if you want user id at front of each row
        datafull.append(data)
        # print('your printing all likes: ', UserLikedNames.objects.filter(user_id=user['id']))
        likes=UserLikedNamesSerializer(UserLikedNames.objects.filter(user_id=user['id']), many=True)
        dislikes=UserDislikedNamesSerializer(UserDislikedNames.objects.filter(user_id=user['id']), many=True)
        for like in likes.data:
            if like['name_id'] in datafull[0]:
                index = datafull[0].index(like['name_id'])
                datafull[userindex][index] = 1
            else:
                datafull[0].append(like['name_id'])
                length=len(datafull[0])
                for index, row in enumerate(datafull):
                    if index==(userindex+1) :
                        row.append(1)
                    elif index !=0:
                        row.append(0)

    # Pull out users if they have no likes
    dataclean=[]
    for index, row in enumerate(datafull):
        if 1 in row[1:] or index==0:
            dataclean.append(row)
    temp=[]
    user_index='Please Like More Names To get Better Recomendations'
    for index, row in enumerate(dataclean):
        if user['id'] in row:
            user_index =index-1
        temp.append(row[1:])
    dataclean=temp
    data_items = pd.DataFrame(dataclean[1:], columns=dataclean[0])
    magnitude = np.sqrt(np.square(data_items).sum(axis=1))

    # unitvector = (x / magnitude, y / magnitude, z / magnitude, ...)
    data_items = data_items.divide(magnitude, axis='index')
    def calculate_similarity(data_items):
        """Calculate the column-wise cosine similarity for a sparse
        matrix. Return a new dataframe matrix with similarities.
        """
        data_sparse = sparse.csr_matrix(data_items)
        similarities = cosine_similarity(data_sparse.transpose())
        sim = pd.DataFrame(data=similarities, index= data_items.columns, columns= data_items.columns)
        return sim

    # Build the similarity matrix
    data_matrix = calculate_similarity(data_items)

    # Lets get the top 10 similar names

    print(data_matrix.loc[13423].nlargest(10))

    #------------------------
    # USER-ITEM CALCULATIONS
    #------------------------

    # Construct a new dataframe with the 10 closest neighbours (most similar)
    # for each artist.
    data_neighbours = pd.DataFrame(index=data_matrix.columns, columns=range(1,11))
    
    for i in range(0, len(data_matrix.columns)):
        data_neighbours.iloc[i,:10] = data_matrix.iloc[0:,i].sort_values(ascending=False)[:10].index

    # Get the artists the user has played.
    # HARD CODED CHANGE FOR FINAL CODE user_index ALREADY SET AND WILL RETURN MORE SWIPES REQUIRED
    # breakpoint()
    try:
        # breakpoint()
        # user_index=user['id']
        # user_index=2
        known_user_likes = data_items.iloc[user_index]
        known_user_likes = known_user_likes[known_user_likes >0].index.values
    except:
        return Response([{"baby_name" : "You need to start swiping before we can recomend choices"}], status=status.HTTP_200_OK)
  
    # Construct the neighbourhood from the most similar items to the
    # ones our user has already liked.
    most_similar_to_likes = data_neighbours.loc[known_user_likes]
    similar_list = most_similar_to_likes.values.tolist()
    similar_list = list(set([item for sublist in similar_list for item in sublist]))
    neighbourhood = data_matrix[similar_list].loc[similar_list]

    # A user vector containing only the neighbourhood items and
    # the known user likes.
    user_vector = data_items.iloc[user_index].loc[similar_list]

    # Calculate the score.
    score = neighbourhood.dot(user_vector).div(neighbourhood.sum(axis=1))

    # Drop the known likes.
    score = score.drop(known_user_likes)

    print(known_user_likes)
    print(score.nlargest(20))
    recomendedwords=score.nlargest(20).index.values.tolist()
    query = BabyNames.objects.filter(id__in=recomendedwords)
    serializer = BabyNamesSerializer(query, many=True)
    # next step is to clean users that do not have any likes then continue with below tutorial 
    # https://medium.com/radon-dev/item-item-collaborative-filtering-with-binary-or-unary-data-e8f0b465b2c3
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_names_from_prefs(request):

    side1 = request.user.couple_user_one.first()
    side2 = request.user.couple_user_two.first()

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

    names_list_full = list(query)
    if len(names_list_full) > 100:
        names_list = random.sample(names_list_full, 100)
    else:
        names_list = names_list_full

    if not UserNamePools.objects.filter(usercouple_id=couple).exists():
        instance = UserNamePools.objects.create(usercouple_id=couple)
        instance.names.set(names_list)
    else:
        instance = UserNamePools.objects.get(usercouple_id=couple)
        instance.names.set(names_list)
    
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

class UserDislikedNamesViewSet(NestedViewSetMixin, viewsets.ModelViewSet):
    queryset = UserDislikedNames.objects.all()
    serializer_class = UserDislikedNamesSerializer

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
    try:
        user2 = User.objects.get(username=request.data['partnerUsername'])
        couple = UserCouples.objects.update_or_create(user_one=request.user, defaults={'user_two':user2})[0]
        couple.save()
        serializer = UserCouplesSerializer(couple)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except:
        return Response("Please Enter a Valid Username", status=status.HTTP_404_NOT_FOUND)
          
    

@csrf_exempt
@api_view(['GET'])
def get_partner(request): 
    if request.user.couple_user_one.first():
        partner_id = request.user.couple_user_one.first().user_two.id
        serializer= UserSerializer(User.objects.get(id=partner_id))
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.user.couple_user_two.first():
        partner_id = request.user.couple_user_two.first().user_one.id
        serializer= UserSerializer(User.objects.get(id=partner_id))
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(False, status=status.HTTP_404_NOT_FOUND)
    

@csrf_exempt
@api_view(['POST'])
def set_preferences(request):
    if request.user.couple_user_one.first():
         usercouple_id = request.user.couple_user_one.first()
    elif request.user.couple_user_two.first():
        usercouple_id = request.user.couple_user_two.first()
    else:
        #Create new couple if non-existing?
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
def deletelikedname(request): # Deletes liked name from user and couple objects
    name = request.data['customName']
    if request.user.couple_user_one.first():
        usercouple_id = request.user.couple_user_one.first()
        if LikedNames.objects.filter(usercouple_id=usercouple_id, name_id=BabyNames.objects.filter(baby_name=name).first()).first():
            couple_likename = LikedNames.objects.filter(usercouple_id=usercouple_id, name_id=BabyNames.objects.filter(baby_name=name).first()).first()
            couple_likename.delete()
    elif request.user.couple_user_two.first():
        usercouple_id = request.user.couple_user_two.first()
        if LikedNames.objects.filter(usercouple_id=usercouple_id, name_id=BabyNames.objects.filter(baby_name=name).first()).first():
            couple_likename = LikedNames.objects.filter(usercouple_id=usercouple_id, name_id=BabyNames.objects.filter(baby_name=name).first()).first()
            couple_likename.delete()

    user_id = request.user.id
    user_likename = UserLikedNames.objects.filter(user_id=user_id, name_id=BabyNames.objects.filter(baby_name=name).first()).first()
    user_likename.delete()

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
    # else:
    #     usercouple_id =''
    user_id = request.user
    name = request.data['customName']
    if(BabyNames.objects.filter(baby_name=name).exists()):
        likename = UserLikedNames.objects.create(user_id=user_id, name_id=BabyNames.objects.filter(baby_name=name).first(), order=UserLikedNames.objects.filter(user_id=user_id).aggregate(Max('order'))['order__max'])

        # likename = UserLikedNames.objects.create(user_id=user_id, name_id=BabyNames.objects.filter(baby_name=name).first(), matched=False, order=UserLikedNames.objects.filter(user_id=1).aggregate(Max('order'))['order__max'])

        likename.save()

    else:
        newName = BabyNames.objects.create(baby_name=name, gender=request.data['gender'], usage='user_added')
        newName.save()
        likename = UserLikedNames.objects.create(user_id=user_id, name_id=newName, order=UserLikedNames.objects.filter(user_id=user_id).aggregate(Max('order'))['order__max'])
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

