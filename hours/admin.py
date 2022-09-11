from django.contrib import admin

from .models import HrsAppResource, ResourceStatus, HrsAppDataType, HrsAppParameter

admin.site.register(HrsAppResource)
admin.site.register(ResourceStatus)
admin.site.register(HrsAppParameter)
admin.site.register(HrsAppDataType)

