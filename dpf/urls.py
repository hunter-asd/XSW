from django.urls import path
from . import views

app_name = "dpf"
urlpatterns = [
    path("", views.dpf_index, name="dpf_index"),
    path("load/<int:shot>", views.dpf_load, name="dpf_load"),
    path("checkshot/", views.check_shot, name="checkshot"),
    path("save/", views.dpf_submit, name="dpf_save"),
]