from django.contrib import admin
from .models import UserPreferences, UserCouple, UserNamesPool, BabyName, LikedName

# Register your models here.
admin.site.register(UserPreferences)
admin.site.register(UserCouple)
admin.site.register(UserNamesPool)
admin.site.register(BabyName)
admin.site.register(LikedName)
