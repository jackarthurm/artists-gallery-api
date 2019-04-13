"""gallery_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from typing import List

from django.conf.urls import url
from django.contrib import admin
from django.urls import (
    path,
    include,
    URLPattern,
)

from rest_framework.routers import DefaultRouter

from email_api.views import CreateContactEnquiryViewSet
from image_api.views import (
    ItemTagViewSet,
    GalleryViewSet,
)
from links_api.views import SocialMediaLinksViewSet


api_router: DefaultRouter = DefaultRouter()
api_router.register(r'image-tags', ItemTagViewSet)
api_router.register(r'gallery-items', GalleryViewSet)
api_router.register(r'contact', CreateContactEnquiryViewSet)
api_router.register(r'social-media-links', SocialMediaLinksViewSet)

urlpatterns: List[URLPattern] = [
    path('', admin.site.urls),
    path('api/', include(api_router.urls))
]
