from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserPreferencesViewSet, UserCouplesViewSet, UserNamePoolsViewSet, BabyNamesViewSet, LikedNamesViewSet
from django.urls import path
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
router.register(r'baby-names', BabyNamesViewSet, basename='baby-names'),

urlpatterns=[
     path('users/', NewUser.as_view()),
     path('pref_names/', get_names_from_prefs)
]

urlpatterns += router.urls
