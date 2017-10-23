from django.shortcuts import render



# Create your views here.


def import_data(request):
    context_dictionary = {}
    return render(request, '', context=context_dictionary)
