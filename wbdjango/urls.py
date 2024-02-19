from django.urls import path, include
from .views import UserAccountListView, ColorUserListView, PostViewSet, GetAllFiles, LoginView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
    path('wbdjango/', UserAccountListView.as_view(), name='user-list'),
    path('color_users/', ColorUserListView.as_view(), name='coloruser-list'),
    path('', include(router.urls)),
    path('songs/', GetAllFiles.as_view(), name='get_all_files'),
    path('login/', LoginView.as_view(), name='login'),
]
