from django.contrib import admin
from .models import contactForm
from .models import Touchpoint
from .models import Graph
from django.utils.safestring import mark_safe
from django.utils.html import format_html

# Register your models here.
# admin.site.register(contactForm)
class TouchpointAdmin(admin.ModelAdmin):
    search_fields = ("action_type", "channel_type", "user_id", "device_category")
    list_display = ("id", "user_id", "visit_time", "active_time", "geo_continent", "geo_country", "action_type", "channel_type", "device_category", "source_name", "experience_emotion")

admin.site.register(Touchpoint, TouchpointAdmin)



class GraphAdmin(admin.ModelAdmin):
    search_fields = ("startDate", "endDate", "runDate")
    list_display = ("id", "runDate", "type", "startDate", "endDate", "link_on_site")
    def link_on_site(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.link)
    link_on_site.allow_tags = True
admin.site.register(Graph, GraphAdmin)