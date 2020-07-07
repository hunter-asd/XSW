from django.shortcuts import redirect,reverse
from django.http import HttpResponse,JsonResponse
from .models import Explog
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

class LogList(ListView):
    model = Explog
    template_name ="LOGSYS/LOG.html"
    paginate_by = 10
    context_object_name = "logs"
    ordering = "shot"
    page_kwarg = "page"

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(LogList,self).get_context_data(**kwargs)
        return context
    def get_queryset(self):
        return Explog.objects.all().order_by("-edit_time")

    @method_decorator(login_required(login_url="../login"))
    def dispatch(self, request, *args, **kwargs):
        return super(LogList,self).dispatch(request, *args, **kwargs)


def save_log(request):
    if request.user.is_authenticated:
        log = Explog.objects.filter(shot=request.POST.get("shot"))
        if log:
            log.update(title=request.POST.get("title"),content=request.POST.get("content"),author=request.user.username)
            return HttpResponse("Update")
        else:
            Explog(shot=request.POST.get("shot"),title=request.POST.get("title"),content=request.POST.get("content"),author=request.user.username).save()
            return HttpResponse("Save")
    else:
        return redirect(reverse("LOGSYS:mylog"))


def detail_log(request,shot):
    if request.user.is_authenticated:
        log_detail=Explog.objects.filter(shot=shot)
        if log_detail:
            return JsonResponse({"shot":log_detail[0].shot,"title":log_detail[0].title,"content":log_detail[0].content})
        else:
            return HttpResponse("")
    else:
        return redirect(reverse("LOGSYS:mylog"))
def search_log(request):
    if request.user.is_authenticated:
        if request.POST.get("shot"):
            log_detail=Explog.objects.filter(shot=request.POST.get("shot"))
            if log_detail:
                return JsonResponse({"shot":log_detail[0].shot,"title":log_detail[0].title,"content":log_detail[0].content,
                                           "author":log_detail[0].author,"time":log_detail[0].edit_time.strftime("%Y-%m-%d %H:%M:%S")})
            else:
                return HttpResponse("NoShot")
    else:
        return redirect(reverse("LOGSYS:mylog"))