from django.shortcuts import render,redirect,reverse
from .dpfFunction import load_xml,get_file_link,save_xml
import os.path
from django.http import JsonResponse
from django.contrib.auth.decorators import  login_required
# Create your views here.
from mds_function import get_current_shot
import xml_function
app_name = "dpf"

@login_required(login_url="../login")
def dpf_index(request):
    return redirect(reverse("dpf:dpf_load", kwargs={"shot":get_current_shot()}))

def check_shot(request):
    shot = request.GET.get("shotnum")
    if os.path.exists(get_file_link("dpf",shot)):
        context = "yes"
    else:
        context = "no"
    return JsonResponse({"exist": context})

def dpf_load(request,shot):
    if request.user.is_authenticated:
        context = xml_function.load_xml(shot,  "DPF")
        return render(request, "dpf/dpf.html", context={"dpf":context})
    else:
        return redirect(reverse("dpf:dpf_index"))
def dpf_submit(request):

    if request.user.is_authenticated:
        save_xml(request)
        return redirect(reverse("dpf:dpf_load",kwargs={"shot": request.POST.get("inputShot")}))
    else:
        return redirect(reverse("dpf:dpf_index"))
