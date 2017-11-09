from allauth.account.decorators import verified_email_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from django_common.mixin import LoginRequiredMixin

from .models import *


class ApplicationListView(LoginRequiredMixin, ListView):
    model = Application
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'


@verified_email_required
def application_view(request):
    applications_list = Application.objects.all()
    f = ApplicationFilter(request.GET, queryset=applications_list)

    paginator = Paginator(f.qs, 25)
    page = request.GET.get('page')
    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        applications = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        applications = paginator.page(paginator.num_pages)

    context_dictionary = {
        'applications': applications,
        'filter': f,
    }
    return render(request, 'applications/application_list.html', context=context_dictionary)
