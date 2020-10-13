from django.shortcuts import render,reverse,redirect
from .acqFunction import save_xml
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
import os.path
import json
from mds_function import get_current_shot,get_effective_newest_shot
from xml_function import get_file_link,load_xml,xml_to_mind,mind_to_xml,save_acq,add_node

# Create your views here.
app_name = "acq"

@login_required(login_url="../login")
def acq_index(request):
    print(get_current_shot())
    return redirect(reverse("acq:acq_load_table", kwargs={"shot": get_current_shot()}))

# def acq_submit(request):
#     if request.user.is_authenticated:
#         save_xml(request)
#         print(request.POST.get("mds"))
#         if request.POST.get("mds") == "UdMDS":
#             update_mds(request)
#         return redirect(reverse("acq:acq_load",kwargs={"shot":request.POST.get("inputShot")}))
#     else:
#         return redirect(reverse("acq:acq_index"))

def acq_submit(request):
    if request.user.is_authenticated:
        source = request.get_raw_uri().split("/")[-2]
        if source=="tree":
            save_xml(request.POST.get("shot"), mind_to_xml(json.loads(request.POST.get("newacq"))).replace("<acq",
                    "<acq xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"acq.xsd\"", 1))
            return JsonResponse({"result": "submit successfully"})
        else:

            data=dict(request.POST)
            print(save_acq(data,request.user))
            return redirect(reverse("acq:acq_load_table",kwargs={"shot":request.POST.get("inputShot")}))
    else:
        return redirect(reverse("acq:acq_index"))


def acq_load(request,shot):
    if request.user.is_authenticated:
        source=request.get_raw_uri().split("/")[-2]
        new_xml_data = load_xml(shot, "acq")
        if source=="tree":
            acqmind=xml_to_mind("acq",new_xml_data)
            acqmind = {"meta": {"name": "ACQ_structural", "author": "liuyong", "version": "1"},
                       "format": "node_tree", "data": acqmind}
            acqmind=str(acqmind).replace("\'", "\"").replace("True", "false")

            return render(request, "acq/APS.html",
                          context={"acqmind": acqmind,"shot":new_xml_data["Header"]["shotnum"]})
        else:
            return render(request, "acq/ACQ.html",
                          context={"data": new_xml_data})
    else:
        return redirect(reverse("acq:acq_index"))

def check_shot(request):
    shot = request.GET.get("shotnum")
    older = str(int(shot) <= get_effective_newest_shot())
    if os.path.exists(get_file_link("acq",shot)):
        context = "yes"
    else:
        context = "no"
    return JsonResponse({"exist": context,"older":older})

def acq_new(request):
    if request.user.is_authenticated:
        new_node=request.POST.get("new_node")
        shot=request.POST.get("shotnum")
        add_node(new_node,shot,"ACQ")
        return JsonResponse({"result": "ok"})
    else:
        return redirect(reverse("acq:acq_index"))

