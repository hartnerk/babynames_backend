from django.contrib import admin
from .models import UserPreferences, UserCouples, UserNamePools, BabyNames, LikedNames

# Register your models here.
admin.site.register(UserPreferences)
admin.site.register(UserCouples)
admin.site.register(UserNamePools)
admin.site.register(BabyNames)
admin.site.register(LikedNames)
