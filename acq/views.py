from django.shortcuts import render,reverse,redirect
from .acqFunction import load_xml,get_file_link,save_xml,update_mds
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
import os.path
from MDSFunction import getCurrentShot,parseNewAcq
# Create your views here.
app_name = "ACQ"

@login_required(login_url="../login")
def acq_index(request):
    return redirect(reverse("ACQ:acq_load", kwargs={"shot": getCurrentShot()}))

def acq_submit(request):
    if request.user.is_authenticated:
        save_xml(request)
        print(request.POST.get("mds"))
        if request.POST.get("mds") == "UdMDS":
            update_mds(request)
        return redirect(reverse("ACQ:acq_load",kwargs={"shot":request.POST.get("inputShot")}))
    else:
        return HttpResponse("git it")

def acq_load(request,shot):
    if request.user.is_authenticated:
        # header, channels = load_xml(shot)
        new_xml_data, _ = parseNewAcq(get_file_link(shot))
        print(new_xml_data)
        return render(request, "ACQ/NewACQ.html",
                      context={"data": new_xml_data})
    else:
        return redirect(reverse("ACQ:acq_index"))

def check_shot(request):
    shot = request.GET.get("shotnum")
    if os.path.exists(get_file_link(shot)):
        context = "yes"
    else:
        context = "no"
    return JsonResponse({"exist": context})

def structural(request,shot):
    if request.user.is_authenticated:
        _,acqmind = parseNewAcq(get_file_link(shot))
        return render(request, "ACQ/AcqMind.html",
                      context={"acqmind": acqmind})
    else:
        return redirect(reverse("ACQ:acq_index"))