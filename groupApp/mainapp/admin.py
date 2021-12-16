from django.contrib import admin
from .models import User, Hobby, FriendRequest


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'image']

admin.site.register(Hobby)

admin.site.register(FriendRequest)