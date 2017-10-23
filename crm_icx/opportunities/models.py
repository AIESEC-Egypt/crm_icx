from django.db import models


# Create your models here.
class ProgramType(models.Model):
    title = models.CharField(max_length=256)


class Opportunity(models.Model):
    title = models.CharField(max_length=256)
    status = models.CharField(max_length=256)

    # DateTime Fields
    latest_end_date = models.DateTimeField()
    earliest_start_date = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    # Foreign Keys
    committee = models.ForeignKey('core.Committee', on_delete=models.CASCADE)
    program_type = models.ForeignKey('ProgramType', on_delete=models.CASCADE)
    applications = models.ForeignKey('applications.Application', on_delete=models.CASCADE)
    op_managers = models.ManyToManyField('people.Manager')
