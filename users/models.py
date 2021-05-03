from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE


# Joins user preferences to built in django user.
# Adds name gender and origin preference fields.
class UserPreferences(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True, 
        blank=True,
        related_name='preferences'
    )
    gender = models.CharField(max_length=15, null=True)
    origin = models.CharField(max_length=30)

    def __str__(self):
        return f'User ID: {self.user} - Preferences: {self.gender}, {self.origin}'


# Join table for two users to reference eachother as partners.
class UserCouple(models.Model):
    user_one = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='couple_user_one'
    )
    user_two = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='couple_user_two'
    )

    def __str__(self):
        return f'Couple {self.id}: {self.user_one} & {self.user_two}'


# Join table for user and their pool of names
# ?? User's pool will be combined with partner's pool on the frontend to create full list of names??
class UserNamesPool(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='names_pool'
    )

    def __str__(self):
        return f'Pool {self.id} - User: {self.user}'


# Stores all baby names.  Pools pull from this list.
class BabyName(models.Model):
    baby_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6,null=True)
    usage = models.CharField(max_length=100)
    pool = models.ForeignKey(
        UserNamesPool,
        on_delete=models.CASCADE,
        related_name='name'
    )

    def __str__(self):
        return f'Baby Name {self.id}: {self.baby_name}'


# Join table for a user and their liked names
class LikedName(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='liked_names'
    )
    liked_name = models.ForeignKey(
        BabyName,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'User: {self.user} - Liked Name: {self.liked_name}'
