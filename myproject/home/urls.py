from django.urls import path
from . import views
from django.contrib import admin

admin.site.site_header = 'Organization Administration'                    # default: "Django Administration"
admin.site.index_title = 'Customer Journey Management'                 # default: "Site administration"
admin.site.site_title = 'Customer Journey Management' # default: "Django site admin"


urlpatterns = [
    path('', views.home),
    path('import-data', views.importData),
    path('export-data', views.exportData),
    path('visualize-graph', views.visualizeGraph),
    path('classify-touchpoint', views.classifyTouchpoint),
    path('predict-touchpoint', views.predictTouchpoint),
    path('cluster-journey', views.clusterJourney),
    path('add-automation-rule', views.automationRule),
    path('upload-file', views.uploadFile),
    path('get-graph', views.getGraph),
    path('get-cluster', views.getCluster),
    path('get-cluster-user-page/<int:id>', views.getClusterUserPage),
    path('cluster-user/<int:id>', views.clusterUser)
]