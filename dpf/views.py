from django.shortcuts import render,redirect,reverse
from .dpfFunction import load_xml,get_file_link,save_xml
import os.path
from django.http import JsonResponse,HttpResponse,Http404
from django.contrib.auth.decorators import  login_required
# Create your views here.
from mds_function import get_current_shot,get_effective_shot_data
import xml_function
from urllib import parse
app_name = "dpf"

@login_required(login_url="../login")
def dpf_index(request):
    return redirect(reverse("dpf:dpf_load", kwargs={"shot":get_current_shot()}))

def check_shot(request):
    shot = request.GET.get("shotnum")
    older=str(int(shot)<=get_effective_shot_data()[0])
    if os.path.exists(get_file_link("dpf",shot)):
        context = "yes"
    else:
        context = "no"
    return JsonResponse({"exist": context,"older":older})

def dpf_load(request,shot):
    if request.user.is_authenticated:
        context = xml_function.load_xml(shot,  "DPF")
        return render(request, "dpf/dpf.html", context={"dpf":context})
    else:
        return redirect(reverse("dpf:dpf_index"))
def dpf_submit(request):

    if request.user.is_authenticated:
        # data=dict(request.POST)
        data = parse.parse_qs(request.POST.get("data").replace("\"", "").strip())
        save_result=xml_function.save_dpf(data,request.user)
        # if validation=="success":
        #     return redirect(reverse("dpf:dpf_load",kwargs={"shot": request.POST.get("inputShot")}))
        # else:
        #     pass
        return JsonResponse({"save_result":save_result})
    else:
        return redirect(reverse("dpf:dpf_index"))
def dpf_new(request):
    if request.user.is_authenticated:
        new_node=request.POST.get("new_node")
        shot=request.POST.get("shotnum")
        xml_function.add_node(new_node,shot,"DPF")
        return JsonResponse({"result": "ok"})
    else:
        return redirect(reverse("dpf:dpf_index"))
