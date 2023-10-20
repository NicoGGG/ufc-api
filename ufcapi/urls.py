"""
URL configuration for ufcapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth.models import User
from ufcscraper.filters import FightFilter
from ufcscraper.models import Event, Fighter, Fight
from django.urls import path, include
from django.db.models import Q

from rest_framework import routers, serializers, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend


# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "location",
            "date",
            "upcoming",
            "link",
            "event_id",
            "name",
            "type",
            "completed",
        ]


class FighterSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name="fighter-detail")

    class Meta:
        model = Fighter
        fields = [
            "id",
            "link",
            "fighter_id",
            "photo_url",
            "first_name",
            "last_name",
            "nickname",
            "height",
            "weight",
            "reach",
            "stance",
            "belt",
            "win",
            "loss",
            "draw",
        ]


class FightSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name="fight-detail")
    fighter = serializers.CharField(source="get_custom_field", read_only=True)

    class Meta:
        model = Fight
        fields = [
            "id",
            "fight_id",
            "weight_class",
            "fighter_one",
            "fighter_two",
            "method",
            "round",
            "time",
            "event",
            "belt",
            "bonus",
            "wl_fighter_one",
            "wl_fighter_two",
            "fighter",
        ]


# Custom field serializer for GET requests
class CustomFieldSerializer(serializers.ModelSerializer):
    fighter = serializers.CharField(source="get_custom_field", read_only=True)

    class Meta:
        model = Fighter
        fields = ["fighter"]


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by("-date")
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["upcoming", "completed", "type"]
    search_fields = ["name", "location"]


class FighterViewSet(viewsets.ModelViewSet):
    queryset = Fighter.objects.all()
    serializer_class = FighterSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["weight", "stance", "belt"]
    search_fields = ["first_name", "last_name", "nickname"]


class FightViewSet(viewsets.ModelViewSet):
    queryset = Fight.objects.all()
    serializer_class = FightSerializer
    filterset_class = FightFilter


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"events", EventViewSet)
router.register(r"fighters", FighterViewSet)
router.register(r"fights", FightViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
