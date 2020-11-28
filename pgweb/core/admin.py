from django import forms
from django.contrib import admin

from pgweb.core.models import Version, OrganisationType, Organisation
from pgweb.core.models import ImportedRSSFeed, ImportedRSSItem
from pgweb.core.models import ModerationNotification


class OrganisationAdminForm(forms.ModelForm):
    class Meta:
        model = Organisation
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(OrganisationAdminForm, self).__init__(*args, **kwargs)


class OrganisationAdmin(admin.ModelAdmin):
    form = OrganisationAdminForm
    list_display = ('name', 'approved', 'lastconfirmed',)
    list_filter = ('approved',)
    ordering = ('name', )
    search_fields = ('name', )
    autocomplete_fields = ['managers', ]


class VersionAdmin(admin.ModelAdmin):
    list_display = ('versionstring', 'reldate', 'supported', 'current', )


admin.site.register(Version, VersionAdmin)
admin.site.register(OrganisationType)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(ImportedRSSFeed)
admin.site.register(ImportedRSSItem)
admin.site.register(ModerationNotification)
