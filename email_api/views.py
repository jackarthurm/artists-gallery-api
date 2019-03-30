from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from email_api.models import ContactEnquiry
from email_api.serializers import ContactEnquirySerializer


class CreateContactEnquiryViewSet(CreateModelMixin, GenericViewSet):

    throttle_scope = 'contact'
    queryset = ContactEnquiry.objects.all()
    serializer_class = ContactEnquirySerializer
