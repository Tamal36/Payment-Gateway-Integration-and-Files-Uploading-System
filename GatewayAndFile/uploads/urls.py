from django.urls import path
from .views import *

urlpatterns = [
    path('upload-view/',    upload_file_view, name='upload-view'), # UI
    path('upload/',         upload_file, name='upload-file'),
    path('files-view/',     list_files_view, name='list-files-view'), # UI
    path('files/',          list_files, name='list-files'),
    path('activity-view/',  list_activity_view, name='list-activity-view'), # UI
    path('activity/',       list_activity, name='list-activity'),
]
