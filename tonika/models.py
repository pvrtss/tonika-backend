from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth import models as user_models
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone


# from django.contrib.auth.hashers import make_password, check_password


class Author(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'authors'

    def __str__(self):
        return '%s (id:%d)' % (self.name, self.id)


class Song(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    chords = models.CharField(max_length=10000)
    cover = models.ImageField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    class Meta:
        managed = True
        db_table = 'songs'


class UserManager(BaseUserManager):
    def _create_user(self, username, password, is_superuser, is_staff, **extra_fields):
        now = timezone.now()
        user = self.model(
            username=username,
            is_superuser=is_superuser,
            is_staff=is_staff,
            last_login=now,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password, **extra_fields):
        return self._create_user(username, password, False, False, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        user = self._create_user(username, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class User(user_models.AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    favourites = models.ManyToManyField(Song)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        managed = True
        db_table = 'users'


class Folder(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'folders'
