from django.db import models
from reports.main import GROUP_TEAM, GROUP_PO, GROUP_INITIATIVE, FLOW_UPSTREAM, FLOW_DOWNSTREAM, FLOW_PRIORITIZED


class FluxoChoice(models.TextChoices):
    UPSTREAM = FLOW_UPSTREAM, 'UpStream'
    DOWNSTREAM = FLOW_DOWNSTREAM, 'DownStream'
    PRIORITIZED = FLOW_PRIORITIZED, 'Priorizados'

class AgrupadoPorChoice(models.TextChoices):
    PO = GROUP_PO, 'PO'
    TEAM = GROUP_TEAM, 'Team'
    INITIATIVE = GROUP_INITIATIVE, 'Iniciativa'