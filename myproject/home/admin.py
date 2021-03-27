from django.contrib import admin
from .models import contactForm
from .models import Touchpoint
from .models import Product
from .models import Transaction
from .models import Post
from .models import Blog
from .models import Review
from .models import Survey
from .models import Advertisement
from .models import Campaign
from .models import LoyaltyProgram
from .models import Mail
from .models import User
from .models import Cluster
from .models import ClusterGraph
from .models import ProcessGraph
from django.utils.safestring import mark_safe
from django.utils.html import format_html

# Register your models here.
# admin.site.register(contactForm)
class TouchpointAdmin(admin.ModelAdmin):
    search_fields = ("action_type", "channel_type", "user_id", "device_category")
    list_display = ("id", "user_link", "visit_time", "active_time", "geo_continent", "geo_country", "action_type", "channel_type", "device_category", "source_name", "interact_item", "user_item", "experience_emotion")
    def interact_item(self, obj):
        if (obj.interract_item_type and obj.interract_item_id):
            link = "/admin/home/" + obj.interract_item_type + "/" + str(obj.interract_item_id)
            return format_html("<a href='{}'>{}</a>", link, obj.interract_item_type)
        else:
            return 'None'

    def user_item(self, obj):
        if (obj.user_item_type and obj.user_item_id):
            link = "/admin/home/" + obj.user_item_type + "/" + str(obj.user_item_id)
            return format_html("<a href='{}'>{}</a>", link, obj.user_item_type)
        else:
            return 'None'

    def user_link(self, obj):
        link = "/admin/home/user/" + str(obj.user_id)
        return format_html("<a href='{}'>{}</a>", link, obj.user_id)

admin.site.register(Touchpoint, TouchpointAdmin)

class ProcessGraphAdmin(admin.ModelAdmin):
    search_fields = ("id", "startDate", "endDate", "runDate", "type", "link",)
    list_display = ("id", "startDate", "endDate", "runDate", "type", "link_on_site")
    def link_on_site(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.link)
    link_on_site.allow_tags = True
admin.site.register(ProcessGraph, ProcessGraphAdmin)


class ClusterGraphAdmin(admin.ModelAdmin):
    search_fields = ("id", "clusterID", "type", "clusterName")
    list_display = ("id", "cluster_link", "clusterNumber" , "clusterName", "type", "link_on_site")
    def cluster_link(self, obj):
        link = "/admin/home/cluster/" + str(obj.clusterID)
        return format_html("<a href='{}'>{}</a>", link, obj.clusterID)
    def link_on_site(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.link)
    link_on_site.allow_tags = True
admin.site.register(ClusterGraph, ClusterGraphAdmin)

class ClusterAdmin(admin.ModelAdmin):
    search_fields = ("startDate", "endDate", "runDate", "algorithm", "preprocessing", "numberClusters")
    list_display = ("id", "runDate", "algorithm", "preprocessing", "numberClusters", "accuracy", "error")
admin.site.register(Cluster, ClusterAdmin)


class UserAdmin(admin.ModelAdmin):
    search_fields = ("id", "username", "email", "phoneNumber")
    list_display = ("id", "username", "email", "phoneNumber", "address")
admin.site.register(User, UserAdmin)

class ProductAdmin(admin.ModelAdmin):
    search_fields = ("id", "name", "category", "price")
    list_display = ("id", "name", "category", "price", "sku", "promotion")
admin.site.register(Product, ProductAdmin)

admin.site.register(Transaction)
admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Review)
admin.site.register(Advertisement)
admin.site.register(Campaign)
admin.site.register(Mail)
admin.site.register(LoyaltyProgram)
admin.site.register(Survey)