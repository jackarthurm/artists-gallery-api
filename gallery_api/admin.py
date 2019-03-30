from django.contrib.admin import AdminSite
from django.conf import settings


class GalleryAPIAdminSite(AdminSite):
    site_header = settings.DJANGO_ADMIN_SITE_HEADER
    site_title = settings.DJANGO_ADMIN_SITE_TITLE
    index_title = settings.DJANGO_ADMIN_SITE_INDEX_TITLE
    site_url = settings.DJANGO_ADMIN_SITE_LINK_URL
