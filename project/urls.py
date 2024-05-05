from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from oauth.views import OAuthLoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('member/', include('member.urls-web')),
    path('mobile/member/', include('member.urls-app')),
    path('accounts/', include('allauth.urls')),
    path('oauth/', include('oauth.urls')),
    path('post/', include('post.urls')),
    path('replies/', include('reply.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
