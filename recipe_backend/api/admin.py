from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class ChefUserAdminConfig(UserAdmin):
    model = ChefUser
    search_fields = ('email', 'first_name', 'username')
    list_display= ('username', 'email', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets

class RecipeAdminConfig(admin.ModelAdmin):
    model = Recipe
    list_display=('title', 'chef')

admin.site.register(ChefUser,ChefUserAdminConfig)
admin.site.register(Recipe, RecipeAdminConfig)