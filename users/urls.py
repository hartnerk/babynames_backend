from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserPreferencesViewSet, UserCoupleViewSet, UserNamesPoolViewSet, BabyNameViewSet, LikedNameViewSet

router = DefaultRouter()

router.register(r'user-list', UserViewSet, basename='user-list'),
router.register(r'preferences', UserPreferencesViewSet,
                basename='preferences'),
router.register(r'couples', UserCoupleViewSet, basename='couples'),
router.register(r'name-pools', UserNamesPoolViewSet, basename='name-pools'),
router.register(r'baby-names', BabyNameViewSet, basename='baby-names'),
router.register(r'liked-names', LikedNameViewSet,
                basename='liked-names')

urlpatterns = router.urls
