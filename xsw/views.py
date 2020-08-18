from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from mds_function import get_effective_newest_shot,get_ip_max_value,get_current_shot,get_exp_time

def mylogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next = request.GET.get("next")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            request.session.set_expiry(60*60)
            if next:
                return redirect(next)
            else:
                return redirect(reverse("home"))
        else:
            return render(request, "Login.html")
    else:
        logout(request)
        return render(request, "Login.html")

@login_required(login_url="../login")
def home(request):
    shot = get_effective_newest_shot()
    # print({"currentshot": shot, "cdate": getExpTime(shot), "maxValue": getIpMaxValue(shot) + "KA"})
    return render(request, "FRC.html", context={"currentshot": shot, "cdate": get_exp_time(shot), "maxValue": get_ip_max_value(shot) + "KA"})
    #return render(request, "xsw.html", context={"currentshot": 5052, "cdate": "2020.04.21 12:45:21", "maxValue": "48"+"KA"})

def mainp(request):
    return redirect("mylogin")
