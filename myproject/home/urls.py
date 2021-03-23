from django.urls import path
from . import views

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
]