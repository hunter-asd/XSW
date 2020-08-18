from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse, JsonResponse
from .function import load_xml, get_file_link, save_xml
from django.contrib.auth.decorators import  login_required
import os.path
# Create your views here.
from MDSFunction import get_current_shot
@login_required(login_url="../login")
def tcn_index(request):
    return redirect(reverse("TCN:tcn_load", kwargs={"shot": get_current_shot()}))


def tcn_load(request, shot):
    if request.user.is_authenticated:
        if not shot:
            shot = 4653
        context = load_xml(shot)
        return render(request, "TCN/TCN.html", context=context)
    else:
        return redirect("TCN:tcn_index")

def check_shot(request):
    shot = request.GET.get("shotnum")
    if os.path.exists(get_file_link("TCN",shot)):
        context = "yes"
    else:
        context = "no"
    return JsonResponse({"exist": context})


def tcn_submit(request):
    if request.user.is_authenticated:
        save_xml(request)
        #context = load_xml(request.POST.get("input-shot"))
        return redirect(reverse("TCN:tcn_load",kwargs={"shot": request.POST.get("input-shot")}))
        #return render(request, "TCN/TCN.html", context=context)
    else:
        return redirect("TCN:tcn_index")


