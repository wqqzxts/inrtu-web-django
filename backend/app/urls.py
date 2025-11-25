"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from characters import views

from rest_framework.routers import DefaultRouter
from characters.api import UserViewset, TeamViewset, PositionViewset, SkillsViewset, ContentTypeViewset, ContentViewset, CharactersViewset, HealthViewset

router = DefaultRouter()
router.register("characters", CharactersViewset, basename="characters")
router.register("teams", TeamViewset, basename="teams")
router.register("positions", PositionViewset, basename="positions")
router.register("skills", SkillsViewset, basename="skills")
router.register("content-types", ContentTypeViewset, basename="content-types")
router.register("content", ContentViewset, basename="content")
router.register("users", UserViewset, basename="users")
router.register("health", HealthViewset, basename="health")


urlpatterns = [
    path('', views.ShowCharactersView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
