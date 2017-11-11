from allauth.account.decorators import verified_email_required
from django.shortcuts import render


# Create your views here.

@verified_email_required
def home(request):
    context_dictionary = {}
    return render(request, 'pages/blue-dashboard.html', context=context_dictionary)


def import_data(request):
    context_dictionary = {}
    return render(request, '', context=context_dictionary)
