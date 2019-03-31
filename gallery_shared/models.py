from uuid import (
    UUID,
    uuid4,
)

from django.db.models import (
    Model,
    UUIDField,
)


class UUIDModel(Model):
    """
    A model with a non-editable UUID that is set only
    once, on saving the model. This is in contrast to
    using the "default" field which causes a UUID to
    be created when instantiating the model class.
    """

    class Meta:
        abstract = True

    id: UUID = UUIDField(
        primary_key=True,
        editable=False,
        verbose_name='Object UUID'
    )

    def save(self, *args, **kwargs) -> None:

        if not self.id:
            self.id = uuid4()

        super(UUIDModel, self).save(*args, **kwargs)
