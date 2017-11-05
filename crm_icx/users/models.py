from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):
    first_name = models.CharField(_('First Name'), max_length=255)
    last_name = models.CharField(_('Last Name'), max_length=255)
    expa_id = models.CharField(max_length=6, unique=True)
    committee = models.ForeignKey('core.Committee', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username

    def profile_filled(self):
        if self.expa_id is not None:
            return True
        return False

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
