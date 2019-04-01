from smtplib import SMTPException
from typing import Dict

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from rest_framework.mixins import CreateModelMixin
from rest_framework.request import Request
from rest_framework.reverse import reverse
from rest_framework.viewsets import GenericViewSet

from email_api.models import ContactEnquiry
from email_api.serializers import ContactEnquirySerializer


class CreateContactEnquiryViewSet(CreateModelMixin, GenericViewSet):

    throttle_scope = 'contact'
    queryset = ContactEnquiry.objects.all()
    serializer_class = ContactEnquirySerializer

    def perform_create(self, serializer):

        obj: ContactEnquiry = serializer.save()

        email: EmailMultiAlternatives = make_new_contact_email(
            obj,
            self.request
        )

        try:
            email.send()
        except SMTPException as e:
            obj.set_email_error(e)
            obj.save(
                update_fields=('email_error',)
            )


def make_new_contact_email(
    obj: ContactEnquiry,
    request: Request
) -> EmailMultiAlternatives:

    index_url: str = reverse(
        'admin:index',
        request=request
    )

    object_url: str = reverse(
        'admin:email_api_contactenquiry_change',
        kwargs=dict(object_id=obj.id),
        request=request
    )

    email_context: Dict[str, str] = dict(
        email=obj.email,
        name=obj.name,
        subject=obj.subject,
        body=obj.body,
        site_name=settings.SITE_NAME,
        object_url=object_url,
        index_url=index_url
    )

    plaintext_template = get_template('new_message_email.txt')
    plaintext_content: str = plaintext_template.render(email_context)

    html_template = get_template('new_message_email.html')
    html_content: str = html_template.render(email_context)

    return EmailMultiAlternatives(
        subject=settings.EMAIL_SUBJECT,
        body=plaintext_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=settings.CONTACT_EMAILS,
        alternatives=[
            (html_content, 'text/html')
        ]
    )
