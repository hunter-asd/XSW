
from django.contrib import admin
from django.urls import path, include
from .views import LogList,save_log,detail_log,search_log

app_name = "log"
urlpatterns = [
    path("", LogList.as_view(), name="mylog"),
    path("save", save_log, name="mylog_save"),
    path("detail/<int:shot>", detail_log, name="mylog_detail"),
    path("search/", search_log, name="mylog_search"),

]

