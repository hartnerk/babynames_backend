from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserPreferences, UserCouples, UserNamePools, BabyNames, LikedNames


class NewUserSerializer(serializers.ModelSerializer):
    # token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    # def get_token(self, obj):
    #     token= {test_token : 'thisisAteesTT'}
    #     return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = User
        fields = ('username', 'password')


class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = ['usercouple_id', 'gender', 'origin']


class BabyNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BabyNames
        fields = ['id', 'baby_name', 'gender', 'usage']


class UserNamePoolsSerializer(serializers.ModelSerializer):
    names = BabyNamesSerializer(many=True)

    class Meta:
        model = UserNamePools
        fields = ['usercouple_id', 'names']


class LikedNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedNames
        fields = ['usercouple_id', 'name_id', 'matched']

    def create(self, validated_data):
        instance, created = self.Meta.model.objects.get_or_create(**validated_data)
        if not created:
            instance.matched = True
            instance.save()
            return instance
        return instance

class UserCouplesSerializer(serializers.ModelSerializer):

    preferences = UserPreferencesSerializer(required=False, read_only=True)
    names_pool = UserNamePoolsSerializer(required=False, read_only=True)
    liked_names = LikedNamesSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = UserCouples
        fields = ['id', 'user_one', 'user_two', 'preferences',
                  'names_pool', 'liked_names']


class UserSerializer(serializers.ModelSerializer):
    couple_user_one = UserCouplesSerializer(many=True, required=False)
    couple_user_two = UserCouplesSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'couple_user_one', 'couple_user_two']