from django.conf.urls.static import static
from django.contrib import admin
from tonika import views as tonika_views, views
from django.urls import include, path
from rest_framework import routers

from tonika_backend import settings

router = routers.DefaultRouter()
router.register(r'songs', tonika_views.SongViewSet)
router.register(r'authors', tonika_views.AuthorViewSet)
router.register(r'folders', tonika_views.FolderViewSet)
router.register(r'users', tonika_views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('upload/', views.upload_image, name="image-upload"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
