import requests
from django.core.exceptions import ObjectDoesNotExist
from django_cron import CronJobBase, Schedule

from django.conf import settings
from crm_icx.core.models import *
from crm_icx.people.models import Manager
from crm_icx.opportunities.models import *


class UpdateOpportunities(CronJobBase):
    RUN_EVERY_MINS = 60 if settings.DEBUG else 10  # 6 hours when not DEBUG

    ALLOW_PARALLEL_RUNS = True
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'core.UpdateOpportunities'

    def do(self):
        opportunities = Opportunity.objects.all().order_by('id')
        for opportunity in opportunities:
            if not opportunity.updated:
                print(opportunity.id)
                response = request_data(opportunity.id)
                update_opportunity(opportunity, response)


def update_opportunity(opportunity, opportunity_data):
    opportunity.created_at = opportunity_data['created_at']
    opportunity.updated_at = opportunity_data['updated_at']

    opportunity_managers_json = opportunity_data['managers']

    if opportunity_managers_json is not None:
        for opportunity_manager_data in opportunity_managers_json:
            opportunity_manager = fetch_manager(opportunity_manager_data)
            opportunity.op_managers.add(opportunity_manager)

    opportunity.updated = True
    opportunity.save()


def create_opportunity_manager(opportunity_manager_data):
    opportunity_manager = Manager(id=opportunity_manager_data['id'])
    opportunity_manager.full_name = opportunity_manager_data['full_name']
    opportunity_manager.email = opportunity_manager_data['email']
    if opportunity_manager_data['contact_info'] is not None:
        try:
            opportunity_manager.phone = opportunity_manager_data['contact_info']['phone']
            opportunity_manager.country_code = opportunity_manager_data['contact_info']['country_code']
        finally:
            pass

    opportunity_manager.save()
    return opportunity_manager


def fetch_manager(opportunity_manager_data):
    op_man_id = opportunity_manager_data['id']
    try:
        opportunity_manager = Manager.objects.get(pk=op_man_id)
    except ObjectDoesNotExist:
        opportunity_manager = create_opportunity_manager(opportunity_manager_data)

    return opportunity_manager


def request_data(opportunity_id, fail=0):
    # Get Access Token
    access_token, created = AccessToken.objects.get_or_create(id=1)
    if created:
        access_token.save()

    # URL Request
    url = 'https://gis-api.aiesec.org//v2/opportunities/' + str(opportunity_id) + \
          '?access_token=' + access_token.value
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    elif fail < 4:
        fail += 1
        print('fail')
        return request_data(opportunity_id, fail)
    else:
        return
