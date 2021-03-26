from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import *

routers = DefaultRouter()
routers.register("users", ChefUserViewSet)
routers.register("recipes", RecipeViewSet)

urlpatterns =[path("", include(routers.urls))]