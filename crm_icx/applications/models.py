from django.db import models


# Create your models here.

class Application(models.Model):
    exchange_participant = models.ForeignKey('people.ExchangeParticipant', on_delete=models.CASCADE)
    date_approved = models.DateTimeField(blank=True, null=True)
    date_realized = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=256)
    experience_start_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
