from django.shortcuts import render,reverse,redirect
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.decorators import login_required
import os.path
import json
from mds_function import get_current_shot,get_effective_shot_data
from xml_function import get_file_link,load_xml,xml_to_mind,mind_to_xml,save_acq,add_node,save_acq_tree
from urllib import parse
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
            save_acq_tree(request.POST.get("shot"), mind_to_xml(json.loads(request.POST.get("newacq"))).replace("<ACQ",
                    "<ACQ xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:noNamespaceSchemaLocation=\"ACQ.xsd\"", 1))
            return JsonResponse({"result": "submit successfully"})
        else:

            # data=dict(request.POST)
            data = parse.parse_qs(request.POST.get("data").replace("\"", "").strip())
            save_result=save_acq(data,request.user)
            # return redirect(reverse("acq:acq_load_table",kwargs={"shot":request.POST.get("inputShot")}))
            return JsonResponse({"save_result":save_result})
    else:
        return redirect(reverse("acq:acq_index"))


def acq_load(request,shot):
    if request.user.is_authenticated:
        source=request.get_raw_uri().split("/")[-2]
        new_xml_data = load_xml(shot, "acq")
        if source=="tree":
            acqmind=xml_to_mind("ACQ",new_xml_data)
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
    older = str(int(shot) <= get_effective_shot_data()[0])
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

