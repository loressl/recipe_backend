from django.urls import include, path
from rest_framework.routers import DefaultRouter

routers = DefaultRouter()

urlpatterns =[path("", include(routers.urls))]