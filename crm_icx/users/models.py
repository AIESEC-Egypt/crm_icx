from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_('Name of User'), blank=True, max_length=255)
    expa_id = models.IntegerField(blank=True)

    def __str__(self):
        return self.username

    def profile_filled(self):
        if (self.expa_id != None and self.name != None):
            return True
        return False

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
