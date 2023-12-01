from django.contrib import admin

from users.models import Config

class ConfigsList(admin.ModelAdmin):
    list_display = ("fk_user", "jira_url", "startdate_field", "duedate_field", "issuetypes", "token")
    list_display_links = ("fk_user", "jira_url", "startdate_field", "duedate_field", "issuetypes", "token")
    search_fields = ("fk_user", "jira_url")
admin.site.register(Config, ConfigsList)