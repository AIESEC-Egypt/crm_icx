from django.db import models
from crm_icx.core.constants import *
import django_filters

# Create your models here.
from crm_icx.core.models import Committee


class Timeline(models.Model):
    # Acceptance Note Signed
    state_an_signed = models.BooleanField(default=False)
    date_an_signed = models.DateTimeField(blank=True, null=True)

    # Withdrawn
    state_withdrawn = models.BooleanField(default=False)
    date_withdrawn = models.DateTimeField(blank=True, null=True)

    # Rejected
    state_rejected = models.BooleanField(default=False)
    date_rejected = models.DateTimeField(blank=True, null=True)

    # Matched
    state_matched = models.BooleanField(default=False)
    date_matched = models.DateTimeField(blank=True, null=True)

    # Accepted
    state_accepted = models.BooleanField(default=False)
    date_accepted = models.DateTimeField(blank=True, null=True)

    # TN Approved
    state_tn_approved = models.BooleanField(default=False)
    date_tn_approved = models.DateTimeField(blank=True, null=True)

    # EP Approved
    state_ep_approved = models.BooleanField(default=False)
    date_ep_approved = models.DateTimeField(blank=True, null=True)

    # EP is Approved
    status_approved = models.BooleanField(default=False)
    date_approved = models.DateTimeField(blank=True, null=True)

    # EP is Realized
    status_realized = models.BooleanField(default=False)
    date_realized = models.DateTimeField(blank=True, null=True)

    # EP is Completed
    status_completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(blank=True, null=True)

    # Experience Start and End Dates
    experience_start_date = models.DateTimeField(blank=True, null=True)
    experience_end_date = models.DateTimeField(blank=True, null=True)

    # Dates that this application was created and updated at
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()


class Application(models.Model):
    status = models.CharField(max_length=256)
    timeline = models.OneToOneField(Timeline, on_delete=models.CASCADE, null=True)
    exchange_participant = models.ForeignKey('people.ExchangeParticipant', on_delete=models.CASCADE)
    opportunity = models.ForeignKey('opportunities.Opportunity', on_delete=models.CASCADE)

    def __str__(self):
        return self.exchange_participant.first_name + ' ' + self.exchange_participant.last_name


class ApplicationFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='iexact')
    status = django_filters.TypedChoiceFilter(choices=APPLICATIONS_STATUSES)

    class Meta:
        model = Application
        fields = ['status',]
