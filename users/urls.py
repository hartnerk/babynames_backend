from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserPreferencesViewSet, UserCouplesViewSet, UserNamePoolsViewSet, BabyNamesViewSet, LikedNamesViewSet

router = DefaultRouter()

router.register(r'user-list', UserViewSet, basename='user-list'),
router.register(r'preferences', UserPreferencesViewSet,
                basename='preferences'),
router.register(r'couples', UserCouplesViewSet, basename='couples'),
router.register(r'name-pools', UserNamePoolsViewSet, basename='name-pools'),
router.register(r'baby-names', BabyNamesViewSet, basename='baby-names'),
router.register(r'liked-names', LikedNamesViewSet,
                basename='liked-names')

urlpatterns = router.urls
