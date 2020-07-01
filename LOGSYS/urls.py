
from django.contrib import admin
from django.urls import path, include
from .views import log

app_name = "LOGSYS"
urlpatterns = [
    path("", log, name="mylog"),

]

