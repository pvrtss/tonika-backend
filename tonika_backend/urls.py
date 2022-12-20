from django.conf.urls.static import static
from django.contrib import admin
from tonika import views as tonika_views, views
from django.urls import include, path
from rest_framework import routers

from tonika_backend import settings

router = routers.DefaultRouter()
router.register(r'songs', tonika_views.SongViewSet, basename='songs')
router.register(r'authors', tonika_views.AuthorViewSet)
# router.register(r'folders', tonika_views.FolderViewSet)
router.register(r'users', tonika_views.UserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/admin/', admin.site.urls),
    path('api/new-songs/', views.NewSongsList.as_view(), name='new'),
    path('api/upload/', views.upload_image, name="image-upload"),
    path('api/auth/', views.AuthView.as_view(), name="auth"),
    path('api/user/create', views.create_user, name="create-user"),
    path('api/logout/', views.logout, name="logout"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
