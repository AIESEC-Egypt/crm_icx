from allauth.account.decorators import verified_email_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

# Create your views here.
from crm_icx.opportunities.models import Opportunity


@verified_email_required
def opportunities_view(request):
    opportunity_list = Opportunity.objects.all()
    # f = ApplicationFilter(request.GET, queryset=applications_list)

    paginator = Paginator(opportunity_list, 25)
    page = request.GET.get('page')
    try:
        opportunities = paginator.page(page)
    except PageNotAnInteger:
        opportunities = paginator.page(1)
    except EmptyPage:
        opportunities = paginator.page(paginator.num_pages)



    context_dictionary = {
        'opportunities': opportunities,
        # 'filter': f,
    }
    return render(request, 'opportunities/opportunities_list.html', context=context_dictionary)
