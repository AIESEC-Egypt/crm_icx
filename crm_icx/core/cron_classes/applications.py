import requests
from crm_icx.applications.models import *
from django.core.exceptions import ObjectDoesNotExist
from django_cron import CronJobBase, Schedule

from django.conf import settings

from crm_icx.core.cron_classes.main import check_home_lc
from crm_icx.core.models import *
from crm_icx.people.models import ExchangeParticipant, Manager
from crm_icx.opportunities.models import *


class UpdateApplications(CronJobBase):
    RUN_EVERY_MINS = 60 if settings.DEBUG else 10  # 6 hours when not DEBUG

    # Additional Settings
    # RUN_AT_TIMES = ['11:30', '14:00', '23:15']
    ALLOW_PARALLEL_RUNS = True

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
    # Initialise Application
    new_application = Application(id=application_data['id'])

    # Exchange Participant Data
    ep_data = application_data['person']
    ep_id = ep_data['id']
    try:
        exchange_participant = ExchangeParticipant.objects.get(pk=ep_id)
    except ObjectDoesNotExist:
        exchange_participant = create_ep(ep_data)
    new_application.exchange_participant = exchange_participant

    # Opportunity Data
    op_data = application_data['opportunity']
    op_id = op_data['id']
    try:
        opportunity = Opportunity.objects.get(pk=op_id)
    except ObjectDoesNotExist:
        opportunity = create_op(op_data)
    new_application.opportunity = opportunity

    # Initialise Timeline for the Application
    timeline = Timeline()
    timeline.date_an_signed = application_data['an_signed_at']
    timeline.date_approved = application_data['date_approved']
    timeline.date_realized = application_data['date_realized']
    timeline.experience_start_date = application_data['experience_start_date']
    timeline.created_at = application_data['created_at']
    timeline.updated_at = application_data['updated_at']
    timeline.save()
    new_application.timeline = timeline

    new_application.status = application_data['status']
    new_application.save()


def update_application(new_application, application_data):
    new_application.timeline.date_approved = application_data['date_approved']
    new_application.timeline.date_realized = application_data['date_realized']
    new_application.timeline.experience_start_date = application_data['experience_start_date']
    new_application.timeline.date_an_signed = application_data['an_signed_at']
    new_application.timeline.updated_at = application_data['updated_at']
    new_application.timeline.save()
    new_application.status = application_data['status']
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


class UpdateSpecificApplication(CronJobBase):
    RUN_EVERY_MINS = 60 if settings.DEBUG else 10  # 6 hours when not DEBUG

    ALLOW_PARALLEL_RUNS = True

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'core.UpdateSpecificApplication'

    def do(self):
        applications = Application.objects.all().distinct('exchange_participant')
        for application in applications:
            if not application.exchange_participant.updated:
                print(application.id)
                response = request_specific_data(application.id)
                update_specific_application(application, response)


def update_specific_application(application, application_data):
    exchange_participant = application.exchange_participant
    exchange_participant_data = application_data['person']

    ep_managers_json = exchange_participant_data['managers']

    if ep_managers_json is not None:
        for ep_manager_data in ep_managers_json:
            ep_manager = fetch_manager(ep_manager_data)
            exchange_participant.ep_managers.add(ep_manager)

    exchange_participant.updated = True
    exchange_participant.save()
    application.save()


def create_ep_manager(ep_manager_data):
    ep_manager = Manager(id=ep_manager_data['id'])
    ep_manager.full_name = ep_manager_data['full_name']
    ep_manager.email = ep_manager_data['email']
    if ep_manager_data['contact_info'] is not None:
        try:
            ep_manager.phone = ep_manager_data['contact_info']['phone']
            ep_manager.country_code = ep_manager_data['contact_info']['country_code']
        finally:
            pass

    ep_manager.save()
    return ep_manager


def fetch_manager(ep_manager_data):
    ep_man_id = ep_manager_data['id']
    try:
        ep_manager = Manager.objects.get(pk=ep_man_id)
    except ObjectDoesNotExist:
        ep_manager = create_ep_manager(ep_manager_data)

    return ep_manager


def request_specific_data(application_id, fail=0):
    # Get Access Token
    access_token, created = AccessToken.objects.get_or_create(id=1)
    if created:
        access_token.save()

    # URL Request
    url = 'https://gis-api.aiesec.org//v2/applications/' + str(application_id) + \
          '?access_token=' + access_token.value
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    elif fail < 4:
        fail += 1
        print('fail')
        return request_specific_data(application_id, fail)
    else:
        return
