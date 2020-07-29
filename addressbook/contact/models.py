from django.db import models
from django.conf import settings


class Contact(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=256)
    value = models.CharField(max_length=256)

    class Meta:
        ordering = ['id']


class ContactList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=256)
    contacts = models.ManyToManyField(Contact)

    class Meta:
        ordering = ['id']
