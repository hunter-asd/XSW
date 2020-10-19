from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse, JsonResponse
# from .function import load_xml, get_file_link, save_xml
from django.contrib.auth.decorators import  login_required
import os.path
import xml_function
from urllib import parse
# from .function import save_xml
# Create your views here.
from mds_function import get_current_shot,get_effective_newest_shot
@login_required(login_url="../login")
def tcn_index(request):
    return redirect(reverse("tcn:tcn_load", kwargs={"shot": get_current_shot()}))


def tcn_load(request, shot):
    if request.user.is_authenticated:
        context = xml_function.load_xml(shot,"TCN")
        return render(request, "tcn/TCN.html", context={"tcn":context})
    else:
        return redirect("tcn:tcn_index")

def check_shot(request):
    shot = request.GET.get("shotnum")
    older = str(int(shot) < get_effective_newest_shot())
    if os.path.exists(xml_function.get_file_link("TCN",shot)):
        context = "yes"
    else:
        context = "no"
    return JsonResponse({"exist": context,"older":older})


def tcn_submit(request):
    if request.user.is_authenticated:
        # data=dict(request.POST.get("data"))
        data=parse.parse_qs(request.POST.get("data").replace("\"","").strip())
        save_result = xml_function.save_tcn(data,request.user)
        # if save_result == "success":
        #     return redirect(reverse("tcn:tcn_load",kwargs={"shot": request.POST.get("input-shot")}))
        # else:
        #     return render(request,"tcn/ErrorPage.html",context={"error":save_result})
        return JsonResponse({"save_result":save_result})
    else:
        return redirect("tcn:tcn_index")


