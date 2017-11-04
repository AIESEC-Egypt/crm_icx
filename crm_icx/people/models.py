from django.db import models


# Create your models here.

class Manager(models.Model):
    full_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    phone = models.CharField(max_length=256, null=True, blank=True)
    country_code = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'


class ExchangeParticipant(models.Model):
    committee = models.ForeignKey("core.Committee", blank=True, null=True, on_delete=models.CASCADE)
    birth_date = models.CharField(max_length=256)
    profile_photo_url = models.URLField()
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=256, blank=True, null=True)
    ep_managers = models.ManyToManyField(Manager)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'Exchange Participant'
        verbose_name_plural = 'Exchange Participants'
