from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.opportunities_view,
        name='opportunities_list'
    ),
]
