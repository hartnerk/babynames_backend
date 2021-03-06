from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Join table for two users to reference eachother as partners.


class UserCouples(models.Model):
    user_one = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='couple_user_one'
    )
    user_two = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='couple_user_two',
        null=True
    )

    def __str__(self):
        return f'Couple {self.id}: {self.user_one} & {self.user_two}'


# Joins user preferences to built in django user.
# Adds name gender and origin preference fields.
class UserPreferences(models.Model):
    usercouple_id = models.OneToOneField(
        UserCouples,
        on_delete=models.CASCADE,
        related_name='preferences',
        primary_key=True
    )
    gender = models.CharField(max_length=15, blank=True)
    origin = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f'UserCouple ID: {self.usercouple_id} - Preferences: {self.gender}, {self.origin}'


# Stores all baby names.  Pools pull from this list.
class BabyNames(models.Model):
    baby_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, null=True, blank=True)
    usage = models.CharField(max_length=100)

    def __str__(self):
        return f'Baby Name {self.id}: {self.baby_name}'


# Join table for user and their pool of names
# ?? User's pool will be combined with partner's pool on the frontend to create full list of names??
class UserNamePools(models.Model):
    usercouple_id = models.OneToOneField(
        UserCouples,
        on_delete=CASCADE,
        related_name='names_pool',
        primary_key=True
    )
    names = models.ManyToManyField(BabyNames, related_name='names_pool')

    def __str__(self):
        return f'Pool {self.usercouple_id} - Names: {self.names}'


# Join table for a user and their liked names
class LikedNames(models.Model):
    
    usercouple_id = models.ForeignKey(
        UserCouples,
        on_delete=models.CASCADE,
        related_name='liked_names'
    )
    name_id = models.ForeignKey(
        BabyNames,
        on_delete=models.CASCADE,
        related_name='liked_names'
    )
    matched = models.BooleanField(null=True, default=False)
    order = models.IntegerField()

    # class Meta:
    #     unique_together = ('usercouple_id', 'name_id')

    def __str__(self):
        return f'UserCouple: {self.usercouple_id} - Liked Name: {self.name_id}'


class UserLikedNames(models.Model):

    user_id = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='user_liked_names')

    name_id = models.ForeignKey(
        BabyNames,
        on_delete=models.CASCADE,
        related_name='user_liked_names'
    )

    order = models.IntegerField()

    def __str__(self):
        return f'User: {self.user_id} - Liked Name: {self.name_id}'

class UserDislikedNames(models.Model):
    user_id = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='user_disliked_names')

    name_id = models.ForeignKey(
        BabyNames,
        on_delete=models.CASCADE,
        related_name='user_disliked_names'
    )

    def __str__(self):
        return f'User: {self.user_id} - Disliked Name: {self.name_id}'