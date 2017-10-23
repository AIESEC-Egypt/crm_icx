import requests
from crm_icx.applications.models import Application
from django.core.exceptions import ObjectDoesNotExist
from django_cron import CronJobBase, Schedule

from django.conf import settings
from .models import AccessToken
from . import create_token
from crm_icx.people.models import ExchangeParticipant


class UpdateAccessToken(CronJobBase):
    RUN_EVERY_MINS = 1 if settings.DEBUG else 60  # 1 hour when not DEBUG
    ALLOW_PARALLEL_RUNS = True
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'core.UpdateAccessToken'

    def do(self):
        self.create_token()

    def create_token(self):
        gis = create_token.GIS()
        access_token, created = AccessToken.objects.get_or_create(id=1)
        access_token.value = gis.generate_token('ali.soliman95@gmail.com', 'thebest1')
        access_token.save()


class UpdateApplications(CronJobBase):
    RUN_EVERY_MINS = 60 if settings.DEBUG else 10  # 6 hours when not DEBUG

    # Additional Settings
    # RUN_AT_TIMES = ['11:30', '14:00', '23:15']
    # ALLOW_PARALLEL_RUNS = True

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'core.UpdateApplications'

    def do(self):
        pages = request_data(1, True)
        print(pages)
        for i in range(1, pages):
            data = request_data(i)
            map_data(data)
            print('Page ' + str(i))


def map_data(r):
    applications = r['data']
    for application in applications:
        application_id = application['id']
        try:
            new_application = Application.objects.get(pk=application_id)
            update_application(new_application, application)
        except ObjectDoesNotExist:
            create_application(application)


def create_application(application_data):
    ep_data = application_data['person']
    ep_id = ep_data['id']
    try:
        exchange_participant = ExchangeParticipant.objects.get(pk=ep_id)
    except ObjectDoesNotExist:
        exchange_participant = create_ep(ep_data)
    new_application = Application(id=application_data['id'])
    new_application.exchange_participant = exchange_participant
    new_application.date_approved = application_data['date_approved']
    new_application.date_realized = application_data['date_realized']
    new_application.status = application_data['status']
    new_application.experience_start_date = application_data['experience_start_date']
    new_application.created_at = application_data['created_at']
    new_application.updated_at = application_data['updated_at']
    new_application.save()


def update_application(new_application, application_data):
    new_application.date_approved = application_data['date_approved']
    new_application.date_realized = application_data['date_realized']
    new_application.status = application_data['status']
    new_application.updated_at = application_data['updated_at']
    new_application.save()


def create_ep(exchange_participant_data):
    exchange_participant = ExchangeParticipant(id=exchange_participant_data['id'])
    exchange_participant.birth_date = exchange_participant_data['dob']
    exchange_participant.profile_photo_url = exchange_participant_data['profile_photo_url']
    exchange_participant.first_name = exchange_participant_data['first_name']
    exchange_participant.last_name = exchange_participant_data['last_name']
    exchange_participant.email = exchange_participant_data['email']
    exchange_participant.save()
    return exchange_participant


    # To do committee
    # exchange_participant.committee =
    # exchange_participant.ep_managers =
    # exchange_participant.phone_number =


def request_data(page, no_of_pages=False):
    ## Get Access Token
    access_token, created = AccessToken.objects.get_or_create(id=1)
    if created:
        access_token.save()

    ## Needed Filters
    filter_data = '&only=data'
    filter_page = '&page=' + str(page)
    filter_created_at_from = '&filters%5Bcreated_at%5D%5Bfrom%5D=' + '2017-09-01'

    ## URL Request
    url = 'https://gis-api.aiesec.org/v2/applications?' \
          'access_token=' + access_token.value + \
          filter_data + \
          filter_page + \
          filter_created_at_from
    r = requests.get(url).json()

    ## Boolean to decide whether I need the number of pages or the data itself
    if no_of_pages:
        pages = r['paging']['total_pages']
        return pages
    else:
        return r
