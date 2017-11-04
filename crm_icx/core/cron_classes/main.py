import requests
from django.core.exceptions import ObjectDoesNotExist
from django_cron import CronJobBase, Schedule

from django.conf import settings
from crm_icx.core.models import *
from crm_icx.core import create_token


class UpdateAccessToken(CronJobBase):
    RUN_EVERY_MINS = 60 if settings.DEBUG else 60  # 1 hour when not DEBUG
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


def check_home_lc(lc_id):
    try:
        committee = Committee.objects.get(pk=lc_id)
        return committee
    except ObjectDoesNotExist:
        request_committees()


def request_committees():
    access_token, created = AccessToken.objects.get_or_create(id=1)

    url = 'https://gis-api.aiesec.org/v2/lists/lcs?access_token=' + access_token.value
    response = requests.get(url).json()
    map_committees(response)

    print('done')


def map_committees(committees):
    for committee in committees:
        child_committee = update_committee(committee['id'],
                                           committee['name'],
                                           committee['tag'])

        if 'parent' in committee:
            if not (committee['parent'] == "null"):
                parent_committee = update_committee(committee['parent']['id'],
                                                    committee['parent']['name'],
                                                    committee['parent']['tag'])
                child_committee.parent_committee = parent_committee
                child_committee.save()


def update_committee(id, name, tag):
    committee, created = Committee.objects.get_or_create(pk=id,
                                                         name=name)
    if tag == 'MC':
        committee.entity_type = 'MC'
    elif tag == 'Region':
        committee.entity_type = 'RE'
    elif tag == 'AI':
        committee.entity_type = 'AI'
    elif tag == 'LC':
        committee.entity_type = 'LC'
    else:
        committee.entity_type = 'XX'
    committee.save()
    return committee
