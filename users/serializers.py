from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserPreferences, UserCouples, UserNamePools, BabyNames, LikedNames


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ['usercouple_id', 'gender', 'origin']


class BabyNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BabyNames
        fields = ['id', 'baby_name', 'gender', 'usage']


class UserNamePoolsSerializer(serializers.ModelSerializer):
    name = BabyNameSerializer(many=True)

    class Meta:
        model = UserNamePools
        fields = ['usercouple_id', 'names']


class LikedNamesSerializer(serializers.ModelSerializer):
    liked_name = BabyNameSerializer()

    class Meta:
        model = LikedNames
        fields = ['usercouple_id', 'name_id']


class UserCouplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCouples
        fields = ['id', 'user_one', 'user_two']


class UserSerializer(serializers.ModelSerializer):
    preferences = UserPreferencesSerializer(many=True, required=False)
    names_pool = UserNamePoolsSerializer(many=True, required=False)
    liked_names = LikedNamesSerializer(many=True, required=False)
    couple_user_one = UserCouplesSerializer(many=True, required=False)
    couple_user_two = UserCouplesSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'preferences',
                  'names_pool', 'liked_names', 'couple_user_one', 'couple_user_two']
