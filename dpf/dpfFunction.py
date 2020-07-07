import xml.etree.cElementTree as ET
from django.conf import  settings
import os.path
from MDSFunction import get_file_link
om_keys = [ 'om-name', 'om-value']
cmd_keys = ['cmd-name', 'cmd-value', 'cmd-incharge', 'cmd-create', 'cmd-db', 'cmd-comment']
pid_keys = ['pid-name', 'pid-p', 'pid-i', 'pid-d', 'pid-rc', 'pid-maxdu', 'pid-fbcstart', 'pid-maxinvang', 'pid-incharge', 'pid-create', 'pid-comment']
el_keys = ['el-name', 'el-value', 'el-incharge', 'el-creat', 'el-comment']
ot_keys = ['ot-name', 'ot-value', 'ot-remark']


def parse_xml(shot):
    file = get_file_link("DPF",shot)
    tree = ET.parse(file)
    root = tree.getroot()
    return root.find("Header").findall("*"), root.findall("OperationMode"),root.findall("Command"),root.findall("PIDcontroller"),root.findall("EngineeringLimit"),root.findall("Other")


def load_xml(shot):
    header, om, cmd, pid, el, ot = parse_xml(shot)

    header = [h.text for h in header]
    om = [{"name":o.find("name").text, "value":o.find("value").text}for o in om]
    cmd = [{"name":c.find("name").text,
            "value":c.find("value").text,
            "personInCharge":c.find("personInCharge").text,
            "implementationHistory":c.find("implementationHistory").text,
            "db":c.find("db").text,
            "comment":c.find("comment").text
            }for c in cmd]
    pid = [{"name":c.find("name").text,
            "P": c.find("P").text,
            "I": c.find("I").text,
            "D": c.find("D").text,
            "RC": c.find("RC").text,
            "maxdU": c.find("maxdU").text,
            "FBStart": c.find("FBStart").text,
            "maxInvAngle": c.find("maxInvAngle").text,
            "personInCharge": c.find("personInCharge").text,
            "implementationHistory": c.find("implementationHistory").text,
            "comment": c.find("comment").text
            } for c in pid]
    el = [{"name":e.find("name").text,
           "value": e.find("value").text,
           "personInCharge": e.find("personInCharge").text,
           "implementationHistory": e.find("implementationHistory").text,
           "comment": e.find("comment").text
           } for e in el]

    ot = [{"name":o.find("name").text,
           "value": o.find("value").text,
           "remark":o.find("remark").text
           } for o in ot]

    return header, om, cmd, pid, el, ot


def save_xml(data):
    tree = ET.parse(os.path.join(settings.BASE_DIR,r"DPF\templates\DPF\ModelDPF.XML"))
    root = tree.getroot()
    header, nodes = root.find("Header").findall("*"), [root.findall("OperationMode"),root.findall("Command"),root.findall("PIDcontroller"),root.findall("EngineeringLimit"),root.findall("Other")]
    for nodek,node in zip([om_keys,cmd_keys,pid_keys,el_keys,ot_keys],nodes):
        for kn in range(len(nodek)):
            d=data.POST.getlist(nodek[kn])
            for i in range(len(d)):
                node[i][kn].text = d[i]
    print(header)
    header[1].text = data.user.username
    header[2].text = data.POST.get("inputShot")
    tree.write(get_file_link(data.POST.get("inputShot")))

