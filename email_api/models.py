from smtplib import (
    SMTPException,
    SMTPResponseException,
)
from typing import (
    Dict,
    Optional,
)

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import (
    EmailField,
    Manager,
    CharField,
    TextField,
    DateTimeField,
)
from django.template.loader import get_template

from gallery_shared.models import UUIDModel


class ContactEnquiry(UUIDModel):

    class Meta:
        verbose_name = 'contact enquiry'
        verbose_name_plural = 'contact enquiries'

    objects = Manager()

    name = CharField(
        max_length=70,
        verbose_name='Contact name'
    )
    email = EmailField(
        max_length=254,
        verbose_name='Contact email address'
    )
    subject = CharField(
        blank=True,
        max_length=78,
        verbose_name='Subject of enquiry'
    )
    body = CharField(
        blank=True,
        max_length=10000,
        verbose_name='Message text'
    )
    email_error = TextField(
        null=True,
        editable=False,
        verbose_name='Email error message'
    )

    created_time = DateTimeField(auto_now_add=True)

    @property
    def email_sent_ok(self) -> Optional[bool]:

        if self.pk:
            return self.email_error is None

    def _create_email(self) -> EmailMultiAlternatives:

        context: Dict[str, str] = dict(
            email=self.email,
            name=self.name,
            subject=self.subject,
            body=self.body
        )

        plaintext_template = get_template('new_message_email.txt')
        plaintext_content: str = plaintext_template.render(context)

        html_template = get_template('new_message_email.html')
        html_content: str = html_template.render(context)

        return EmailMultiAlternatives(
            subject=self.subject,
            body=plaintext_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=settings.CONTACT_EMAILS,
            alternatives=[
                (html_content, 'text/html')
            ]
        )

    def _set_email_error(self, e: SMTPException):

        if isinstance(e, SMTPResponseException):

            smtp_err: str = e.smtp_error.decode('utf-8')

            err_text: str = (
                f'SMTP response error with status code {e.smtp_code} - '
                f'"{smtp_err}"'
            )

        else:
            err_text: str = f'SMTP error - "{e}"'

        self.email_error = err_text

    def save(self, *args, **kwargs) -> None:

        email: EmailMultiAlternatives = self._create_email()

        try:
            email.send()

        except SMTPException as e:
            self._set_email_error(e)

        super(ContactEnquiry, self).save(*args, **kwargs)

    def __str__(self) -> str:

        return f'Message from "{self.name}"'
