from allauth.account.decorators import verified_email_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

# Create your views here.
from crm_icx.people.models import ExchangeParticipant


@verified_email_required
def home(request):
    eps_list = ExchangeParticipant.objects.all()
    paginator = Paginator(eps_list, 25)
    page = request.GET.get('page')
    try:
        eps = paginator.page(page)
    except PageNotAnInteger:
        eps = paginator.page(1)
    except EmptyPage:
        eps = paginator.page(paginator.num_pages)

    context_dictionary = {'eps': eps,
                          }
    return render(request, 'pages/blue-dashboard.html', context=context_dictionary)


def import_data(request):
    context_dictionary = {}
    return render(request, '', context=context_dictionary)
