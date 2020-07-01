import xml.etree.cElementTree as ET
import os.path
from django.conf import settings
from operator import itemgetter

nodes = ["name", "id", "initialValue", "timeUnit", "division", "personInCharge", "toPosition", "insituPosition", "implementationHistory",
         "comment", "isSigmaInverse", "isInverse", "andSignalName", "ContinuousSigma1Check", "isProtection", "delayTime",
         "repeatNumber", "timingMode", "startTime", "lowWidth", "highWidth"]

def get_file_link(shot):
    path = settings.XMLPATH
    folder = ("00000"+str(int(shot)//200*200))[-5:]
    link = os.path.join(path,folder,"tcn",("00000"+str(shot))[-5:]+"OUT.xml")
    return link

def parse_xml(shot):

    file = get_file_link(shot)
    tree = ET.parse(file)
    root = tree.getroot()
    return root.find("Header").findall("*"), root.findall("outputSignal")

def load_xml(shot="4653"):
    head, channels = parse_xml(shot)
    data=[]
    for c in channels:
        cdata = {}
        for n in nodes:
            cdata[n] = next(c.iter(n)).text
        data.append(cdata)
    data.sort(key=lambda cd:cd["id"])
    choose_button = [c["name"] for c in data]
    block1, block2, block3 = choose_button[:11], choose_button[11:22], choose_button[22:]
    header = [h.text for h in head]
    return {"block1": block1, "block2": block2, "block3": block3, "data": data, "header": header}

def save_xml(data):
    tree = ET.parse(os.path.join(settings.BASE_DIR, r"TCN\templates\TCN\TcnModel.XML"))
    root = tree.getroot()
    for n in nodes:
        for d,nde in zip(data.POST.getlist(n), list(root.iter(n))):
            nde.text = d
    next(root.iter("shotnum")).text = data.POST.get("input-shot")
    next(root.iter("operator")).text = data.user.username
    tree.write(get_file_link(data.POST.get("input-shot")))
