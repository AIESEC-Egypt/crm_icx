import datetime

from crm_icx.opportunities.models import ProgramType
from crm_icx.core.models import APIRequest

start_date = datetime.date(year=2017, month=11, day=1)
end_date = datetime.date(year=2017, month=11, day=30)
api_request = APIRequest(name='NOV17', type=1, start_date=start_date, end_date=end_date)
api_request.save()

gv = ProgramType(id=1, title='Global Volunteer')
ge = ProgramType(id=5, title='Global Entrepreneur')
gt = ProgramType(id=2, title='Global Talent')

gv.save()
ge.save()
gt.save()
