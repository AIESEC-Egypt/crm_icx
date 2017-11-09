from django.db import models


# Create your models here.
class ProgramType(models.Model):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Program Type'
        verbose_name_plural = 'Program Types'


class Opportunity(models.Model):
    title = models.CharField(max_length=256)
    status = models.CharField(max_length=256)

    # DateTime Fields
    latest_end_date = models.DateTimeField()
    earliest_start_date = models.DateTimeField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    updated = models.BooleanField(default=False)

    # Foreign Keys
    committee = models.ForeignKey('core.Committee', on_delete=models.CASCADE)
    program_type = models.ForeignKey('ProgramType', on_delete=models.CASCADE)
    op_managers = models.ManyToManyField('people.Manager')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Opportunity'
        verbose_name_plural = 'Opportunities'
