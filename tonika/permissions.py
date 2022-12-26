from rest_framework import permissions
from tonika.models import User
import redis

from tonika_backend import settings

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


class ManagerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        ssid = request.COOKIES.get("session_id")
        if ssid is not None:
            uname = session_storage.get(ssid)
            if uname is not None:
                uname = uname.decode()
                user = User.objects.get(username=uname)
                if user.is_superuser or user.is_staff:
                    return True
        return False
        

class ManagerAndUserCreateOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        ssid = request.COOKIES.get("session_id")
        if ssid is not None:
            uname = session_storage.get(ssid)
            if uname is not None:
                uname = uname.decode()
                user = User.objects.get(username=uname)
                if user is not None and request.method == 'POST':
                    return True
                if user.is_superuser or user.is_staff:
                    return True
        return False


class ManagerOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        ssid = request.COOKIES.get("session_id")
        if ssid is not None:
            uname = session_storage.get(ssid)
            if uname is not None:
                uname = uname.decode()
                user = User.objects.get(username=uname)
                if user.is_superuser or user.is_staff:
                    return True
        return False


class DefaultUser(permissions.BasePermission):
    def has_permission(self, request, view):
        ssid = request.COOKIES.get("session_id")
        if ssid is not None:
            uname = session_storage.get(ssid)
            if uname is not None:
                return True
        return False
