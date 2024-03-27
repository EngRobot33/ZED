import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile_photo = models.ImageField(verbose_name=_('user profile photo'), upload_to='profile_photos/', blank=True,
                                      null=True)
    banner_photo = models.ImageField(verbose_name=_('user banner photo'), upload_to='banner_photos/', blank=True,
                                     null=True)
    bio = models.TextField(verbose_name=_('user bio'), null=True, blank=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        db_table = "User"

    def __str__(self):
        if self.first_name and self.last_name:
            full_name = "%s %s" % (self.first_name, self.last_name)
            return full_name.strip()
        else:
            username = "%s" % (self.username,)
            return username.strip()
