from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import ActivateUser

from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/drf-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('accounts/activate/<uid>/<token>', ActivateUser.as_view({'get': 'activation'}), name='activation'),

    path('api/', include('wbdjango.urls')),

    path('api/', include('parser_app.urls')),

    path('api/file/', include(('wbdjango.urls', 'file'), namespace='file')),

]

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]