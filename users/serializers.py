from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserPreferences, UserCouple, UserNamesPool, BabyName, LikedName


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ['id', 'user', 'gender', 'origin']


class BabyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = BabyName
        fields = ['id', 'baby_name', 'gender', 'usage']


class UserNamesPoolSerializer(serializers.ModelSerializer):
    name = BabyNameSerializer(many=True)

    class Meta:
        model = UserNamesPool
        fields = ['id', 'name']


class LikedNameSerializer(serializers.ModelSerializer):
    liked_name = BabyNameSerializer()

    class Meta:
        model = LikedName
        fields = ['id', 'liked_name']


class UserCoupleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCouple
        fields = ['id', 'user_one', 'user_two']


class UserSerializer(serializers.ModelSerializer):
    preferences = UserPreferencesSerializer(many=True, required=False)
    names_pool = UserNamesPoolSerializer(many=True, required=False)
    liked_names = LikedNameSerializer(many=True, required=False)
    couple_user_one = UserCoupleSerializer(many=True, required=False)
    couple_user_two = UserCoupleSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'preferences',
                  'names_pool', 'liked_names', 'couple_user_one', 'couple_user_two']
