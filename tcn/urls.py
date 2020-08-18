from django.urls import path
from . import views

app_name = "tcn"
urlpatterns = [
    path("", views.tcn_index, name="tcn_index"),
    # path("load/", views.tcn_index, name="tcn_index"),
    path("save/", views.tcn_submit, name="tcn_save"),
    path("load/<int:shot>", views.tcn_load, name="tcn_load"),
    path("checkshot/", views.check_shot, name="check_shot"),
    ]
