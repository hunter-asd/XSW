from django.shortcuts import render,redirect,reverse
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from mds_function import get_effective_shot_data

def mylogin(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next = request.GET.get("next")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            request.session.set_expiry(24*60*60)
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
    shot,cdate,maxValue=get_effective_shot_data()
    # print({"currentshot": shot, "cdate": getExpTime(shot), "maxValue": getIpMaxValue(shot) + "KA"})
    return render(request, "FRC.html", context={"currentshot": str(shot), "cdate": cdate, "maxValue": maxValue + "KA"})
    #return render(request, "FRC.html", context={"currentshot": 5052, "cdate": "2020.04.21 12:45:21", "maxValue": "48"+"KA"})

def mainp(request):
    return redirect("mylogin")
