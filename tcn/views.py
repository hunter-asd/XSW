from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse, JsonResponse
# from .function import load_xml, get_file_link, save_xml
from django.contrib.auth.decorators import  login_required
import os.path
import xml_function
# from .function import save_xml
# Create your views here.
from mds_function import get_current_shot
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
    if os.path.exists(xml_function.get_file_link("tcn",shot)):
        context = "yes"
    else:
        context = "no"
    return JsonResponse({"exist": context})


def tcn_submit(request):
    if request.user.is_authenticated:
        xml_function.save_xml("TCN",request.POST.copy())
        return redirect(reverse("tcn:tcn_load",kwargs={"shot": request.POST.get("input-shot")}))
    else:
        return redirect("tcn:tcn_index")


