from django.contrib.admin import site

from email_api.models import ContactEnquiry


site.register(ContactEnquiry)
