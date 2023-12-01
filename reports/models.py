from django.db import models

class FluxoChoice(models.TextChoices):
    UPSTREAM = 'upstream', 'UpStream'
    DOWNSTREAM = 'downstream', 'DownStream'

class AgrupadoPorChoice(models.TextChoices):
    PO = 'po', 'PO'
    TEAM = 'team', 'Team'