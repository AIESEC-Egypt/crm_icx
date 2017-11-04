import requests
from crm_icx.applications.models import Application
from django.core.exceptions import ObjectDoesNotExist
from django_cron import CronJobBase, Schedule

from django.conf import settings

from crm_icx.core.cron_classes.main import check_home_lc
from crm_icx.core.models import *
from crm_icx.people.models import ExchangeParticipant
from crm_icx.opportunities.models import *


class UpdateApplications(CronJobBase):
    RUN_EVERY_MINS = 60 if settings.DEBUG else 10  # 6 hours when not DEBUG

    # Additional Settings
    # RUN_AT_TIMES = ['11:30', '14:00', '23:15']
    # ALLOW_PARALLEL_RUNS = True

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'core.UpdateApplications'

    def do(self):
        requests = create_requests()
        for request in requests:
            for i in range(request.current_page, request.total_pages + 1):
                response = request_data(i, request=request)
                map_applications(response, request)
                print('Page ' + str(i) + ', Request Current Page is: ' + str(request.current_page))
        reset_requests(requests)


def reset_requests(requests):
    for applications_request in requests:
        applications_request.current_page = 1
        applications_request.save()


def create_requests():
    applications_requests = APIRequest.objects.filter(type=1)
    for applications_request in applications_requests:
        applications_request.total_pages = request_data(1, True, applications_request)
        applications_request.save()
    return applications_requests


def map_applications(response, request):
    applications = response['data']
    for application in applications:
        application_id = application['id']
        try:
            new_application = Application.objects.get(pk=application_id)
            update_application(new_application, application)
        except ObjectDoesNotExist:
            create_application(application)
    request.current_page = request.current_page + 1
    request.save()


def create_application(application_data):
    # Exchange Participant Data
    ep_data = application_data['person']
    ep_id = ep_data['id']
    try:
        exchange_participant = ExchangeParticipant.objects.get(pk=ep_id)
    except ObjectDoesNotExist:
        exchange_participant = create_ep(ep_data)

    # Opportunity Data
    op_data = application_data['opportunity']
    op_id = op_data['id']
    try:
        opportunity = Opportunity.objects.get(pk=op_id)
    except ObjectDoesNotExist:
        opportunity = create_op(op_data)

    new_application = Application(id=application_data['id'])
    new_application.exchange_participant = exchange_participant
    new_application.opportunity = opportunity
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

    home_lc_json = exchange_participant_data['home_lc']
    if home_lc_json is not None:
        home_lc_id = home_lc_json['id']
        check_home_lc(home_lc_id)
        home_lc = Committee.objects.get(pk=home_lc_id)
        exchange_participant.committee = home_lc

    exchange_participant.save()

    return exchange_participant

def create_op(opportunity_data):
    opportunity = Opportunity(id=opportunity_data['id'])
    opportunity.title = opportunity_data['title']
    opportunity.status = opportunity_data['status']
    opportunity.program_type = ProgramType.objects.get(pk=opportunity_data['programmes']['id'])
    opportunity.earliest_start_date = opportunity_data['earliest_start_date']
    opportunity.latest_end_date = opportunity_data['latest_end_date']
    opportunity.committee = Committee.objects.get(pk=opportunity_data['office']['id'])
    opportunity.save()

    return opportunity

def request_data(page, no_of_pages=False, request=None):
    # Get Access Token
    access_token, created = AccessToken.objects.get_or_create(id=1)
    if created:
        access_token.save()

    # Needed Filters
    filter_data = '&only=data'
    filter_page = '&page=' + str(page)
    filter_created_at_from = '&filters%5Bcreated_at%5D%5Bfrom%5D=' + str(request.start_date)
    filter_created_at_to = '&filters%5Bcreated_at%5D%5Bto%5D=' + str(request.end_date)
    filter_for_opportunities = '&filters%5Bfor%5D=opportunities'

    # URL Request
    url = 'https://gis-api.aiesec.org/v2/applications?' \
          'access_token=' + access_token.value + \
          filter_data + \
          filter_page + \
          filter_created_at_from + \
          filter_created_at_to + \
          filter_for_opportunities
    r = requests.get(url).json()

    # Boolean to decide whether I need the number of pages or the data itself
    if no_of_pages:
        pages = r['paging']['total_pages']
        return pages
    else:
        return r
