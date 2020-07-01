from django.urls import path
from . import views

app_name = "ACQ"
urlpatterns = [
    path("", views.acq_index, name="acq_index"),
    path("load/<int:shot>", views.acq_load, name="acq_load"),
    path("checkshot/", views.check_shot, name="checkshot"),
    path("save/", views.acq_submit, name="acq_save"),
    path("structural/<int:shot>", views.structural, name="acq_structural"),
]