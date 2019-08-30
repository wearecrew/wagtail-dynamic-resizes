from django.urls import re_path

from .views import DynamicResizes


urlpatterns = [
    re_path(r"^(\d+)/([a-z0-9\-]+)/$", DynamicResizes.as_view(), name="permitted_images")
]
