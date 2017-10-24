from django.db import models


# Create your models here.
class Committee(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    parent_committee = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)

    # Entity Type
    entity_type_choices = (
        ('AI', 'AIESEC INTERNATIONAL'),
        ('RE', 'Regional'),
        ('MC', 'Members Committee'),
        ('LC', 'Local Committee'),
        ('XX', 'Type Unknown')
    )
    entity_type = models.CharField(max_length=2, choices=entity_type_choices, default='XX')

    def __str__(self):
        return self.name



class AccessToken(models.Model):
    value = models.TextField()

    def __str__(self):
        return 'Access Token ' + str(self.id)

    class Meta:
        verbose_name = 'Access Token'
        verbose_name_plural = 'Access Token'


class APIRequest(models.Model):
    name = models.CharField(max_length=256)
    current_page = models.IntegerField(default=1)
    total_pages = models.IntegerField(default=1)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = 'API Request'
        verbose_name_plural = 'API Requests'

