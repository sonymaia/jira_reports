from django.db import models
from django.contrib.auth.models import User

class Config(models.Model):
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, default = "")
    token = models.BinaryField()
    jira_url = models.TextField(default="https://jiraps.atlassian.net")
    startdate_field = models.TextField(default="customfield_10015")
    duedate_field = models.TextField(default="duedate")
    issuetypes = models.TextField(default="Story")
    
    def __str__(self):
        return f"Config [token = {self.token}]"