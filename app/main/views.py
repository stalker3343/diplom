import os
import re

from django.shortcuts import render, redirect
from .forms import RFPAuthForm, ParametersScan
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from .models import CVES, ResultScan, InfectionRate, Protocols
from .tasks.tasks import tasks


TEMPLATE_FOR_DEFINE_IP_ADDRESS = re.compile(
            r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
        )


def index(request):
    return render(request, "main/welcome.html")


def login_request(request):
    if request.method == "POST":
        form = RFPAuthForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return redirect("/home")
            else:
                messages.error(request, "Invalid username and password")
                return redirect("/login")
        else:
            messages.error(request, "Invalid username and password")
            return redirect("/login")
    form = RFPAuthForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/login")


def home_page(request):
    if request.method == "POST":
        data = request.POST
        run_task(data)
    users = ResultScan.objects.all()
    return render(request=request, template_name="main/home.html", context={"users": users})


def scan(request):
    form = ParametersScan(ip_targets=tuple(define_targets()), cve_list=tuple(get_cves()))
    if request.GET:
        temp = request.GET["ip_targets"]
        print(temp)
    return render(request, template_name="main/scan.html", context={"scan_form": form})


def define_targets():
    from django.conf import settings
    content_from_file = open(str(settings.BASE_DIR) + '/result.txt', "r").read().split("\n")
    return [(str(ind), element) for ind, element in enumerate(content_from_file)]


def get_cves():
    cves = CVES.objects.all()
    return [(str(elem.id), elem.CVE_id) for elem in cves]


def run_task(data):
    ip_targets = tuple(define_targets())
    cve_list = tuple(get_cves())
    # print(cve_list)

    ip_target = get_elem_for_task(ip_targets, data["ip_target"])
    cve = get_elem_for_task(cve_list, data["cve"])
    cve = "CVE-2022-21907"
    #ip_target = "192.168.1.103"
    ip_target = "192.168.1.103"
    values_from_cve = CVES.objects.filter(CVE_id=cve).values()[0]
    print(values_from_cve,cve)

    protocol = str(Protocols.objects.get(pk=values_from_cve.get("protocol_id_id")))
    result_task = tasks.get(values_from_cve.get("name"))(ip_target, False)
    print(result_task)
    gradation = InfectionRate.objects.filter(pk=result_task).values()[0].get("gradation")
    result_scan = ResultScan.objects.create(ip_target=ip_target, cve_id=cve, protocol=protocol, gradation=gradation)
    result_scan.save()


def get_elem_for_task(elem_form: tuple, key: str):
    for elem in elem_form:
        # print(elem[0],key)
        if elem[0].find(key):
            return elem[1]
