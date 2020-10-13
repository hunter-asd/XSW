from django.urls import path
from . import views

app_name = "acq"
urlpatterns = [
    path("", views.acq_index, name="acq_index"),
    path("load/tree/<int:shot>", views.acq_load, name="acq_load_tree"),
    path("load/table/<int:shot>", views.acq_load, name="acq_load_table"),
    path("load/checkshot/", views.check_shot, name="checkshot"),
    path("save/tree/", views.acq_submit, name="acq_save_tree"),
    path("save/table", views.acq_submit, name="acq_save_table"),
    path("new/", views.acq_new, name="acq_new"),
]