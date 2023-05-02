from django.contrib import admin
from users.models import User
from products.admin import BasketAdmin


# admin.site.register(User)
# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (BasketAdmin,)
