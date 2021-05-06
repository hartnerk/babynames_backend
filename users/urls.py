from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserPreferencesViewSet, UserCouplesViewSet, UserNamePoolsViewSet, BabyNamesViewSet, LikedNamesViewSet
from django.urls import path
from . import views
from .views import NewUser, get_names_from_prefs
from rest_framework_extensions.routers import NestedRouterMixin


class NestedDefaultRouter(NestedRouterMixin, DefaultRouter):
     pass

router = NestedDefaultRouter()

couples_router = router.register(r'couples', UserCouplesViewSet, basename='couples')

couples_router.register(r'liked-names', LikedNamesViewSet,
                basename='liked-names', parents_query_lookups=['usercouple_id']),
couples_router.register(r'preferences', UserPreferencesViewSet,
                basename='preferences', parents_query_lookups=['usercouple_id']),
couples_router.register(r'name-pools', UserNamePoolsViewSet, basename='name-pools', parents_query_lookups=['usercouple_id']),

router.register(r'user-list', UserViewSet, basename='user-list'),
# router.register(r'preferences', UserPreferencesViewSet,
#                 basename='preferences'),
# router.register(r'couples', UserCouplesViewSet, basename='couples'),
# router.register(r'name-pools', UserNamePoolsViewSet, basename='name-pools'),
router.register(r'baby-names', BabyNamesViewSet, basename='baby-names'),

urlpatterns=[
     path('users/', views.NewUser.as_view()),
     path('set_couples/', views.set_couple, name='set_couple'),
     path('set_preferences/', views.set_preferences, name='set_preferences'),
     path('pref_names/', get_names_from_prefs)
]

urlpatterns += router.urls
