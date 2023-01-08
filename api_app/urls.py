from django.urls import path

from .views import ObjectsView

urlpatterns = [
    path("objects/", ObjectsView.as_view(), name="earth_objects"),
]
