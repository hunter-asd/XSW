from django.shortcuts import render,reverse,redirect
from .acqFunction import save_xml
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import os.path
import json
# from .acqFunction import load_xml,mind_to_xml
from mds_function import get_current_shot
from xml_function import get_file_link,load_xml,xml_to_mind,mind_to_xml

# Create your views here.
app_name = "acq"

@login_required(login_url="../login")
def acq_index(request):
    print(get_current_shot())
    return redirect(reverse("acq:acq_load", kwargs={"shot": get_current_shot()}))

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
        save_xml(request.POST.get("shot"), mind_to_xml(json.loads(request.POST.get("newacq"))).replace("<acq",
                "<acq xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"acq.xsd\"", 1))
        return JsonResponse({"result": "submit successfully"})
    else:
        return redirect(reverse("acq:acq_index"))


def acq_load(request,shot):
    if request.user.is_authenticated:
        new_xml_data=load_xml(shot,"ACQ")
        acqmind=xml_to_mind("ACQ",new_xml_data)
        acqmind = {"meta": {"name": "ACQ_structural", "author": "liuyong", "version": "1"},
                   "format": "node_tree", "data": acqmind}
        acqmind=str(acqmind).replace("\'", "\"").replace("True", "false")
        datatype=1
        if datatype:
            return render(request, "acq/APS.html",
                          context={"acqmind": acqmind,"shot":new_xml_data["Header"]["shotnum"]})
        else:
            return render(request, "acq/NewACQ.html",
                          context={"data": new_xml_data})
    else:
        return redirect(reverse("acq:acq_index"))

def check_shot(request):
    shot = request.GET.get("shotnum")
    if os.path.exists(get_file_link("acq",shot)):
        context = "yes"
    else:
        context = "no"
    return JsonResponse({"exist": context})

