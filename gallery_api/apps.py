from django.contrib.admin.apps import AdminConfig


class GalleryAPIAdminConfig(AdminConfig):
    default_site = 'gallery_api.admin.GalleryAPIAdminSite'
