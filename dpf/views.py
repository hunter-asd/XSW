from django.shortcuts import render,redirect,reverse
from .dpfFunction import load_xml,get_file_link,save_xml
import os.path
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import  login_required
# Create your views here.
from mds_function import get_current_shot
app_name = "dpf"

@login_required(login_url="../login")
def dpf_index(request):
    return redirect(reverse("DPF:dpf_load", kwargs={"shot":get_current_shot()}))

def check_shot(request):
    shot = request.GET.get("shotnum")
    if os.path.exists(get_file_link("dpf",shot)):
        context = "yes"
    else:
        context = "no"
    return JsonResponse({"exist": context})

def dpf_load(request,shot):
    if request.user.is_authenticated:
        header, om, cmd, pid, el, ot = load_xml(shot)
        return render(request, "DPF/DPF.html",
                      context={"header": header, "om": om, "cmd": cmd, "pid": pid, "el": el, "ot": ot})
    else:
        return redirect(reverse("DPF:dpf_index"))
def dpf_submit(request):

    if request.user.is_authenticated:
        save_xml(request)
        return redirect(reverse("DPF:dpf_load",kwargs={"shot": request.POST.get("inputShot")}))
    else:
        return redirect(reverse("DPF:dpf_index"))
