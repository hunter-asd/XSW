import xml.etree.cElementTree as ET
from django.conf import settings
import os.path
import numpy as np
import MDSplus

nodes = ['channelDescription', 'ChnlName', 'Unit', 'ChnlId', 'Len', 'Post', 'MaxDat', 'Freq', 'LowRang', 'HighRang', 'Factor', 'Offset', 'Dly', 'DatAttr', 'DatWth', 'division', 'personInCharge', 'fromPosition', 'insituPosition', 'implementationHistory']
mds_nodes=['Unit','LowRang', 'HighRang', 'Factor', 'Offset','MaxDat']
def get_file_link(shot):
    path = settings.XMLPATH
    folder = ("00000"+str(int(shot)//200*200))[-5:]
    link = os.path.join(path,folder,"ACQ",("00000"+str(shot))[-5:]+"ACQ.xml")
    return link

def parse_xml(shot):
    file = get_file_link(shot)
    tree = ET.parse(file)
    root = tree.getroot()
    return root.find("Header").findall("*"), root.findall("Channel")

def load_xml(shot):
    header, channel = parse_xml(shot)
    header = [h.text for h in header]
    channels = [{"ChnlName": c.find("ChnlName").text,
                "Unit": c.find("Unit").text,
                "ChnlId": c.find("ChnlId").text,
                "Len": c.find("Len").text,
                "Post": c.find("Post").text,
                "MaxDat": c.find("MaxDat").text,
                "Freq": c.find("Freq").text,
                "LowRang": c.find("LowRang").text,
                "HighRang": c.find("HighRang").text,
                "Factor": c.find("Factor").text,
                "Offset": c.find("Offset").text,
                "Dly": c.find("Dly").text,
                "DatAttr": c.find("DatAttr").text,
                "DatWth": c.find("DatWth").text,
                "division": c.find("division").text,
                "personInCharge": c.find("personInCharge").text,
                "fromPosition": c.find("fromPosition").text,
                "insituPosition": c.find("insituPosition").text,
                "implementationHistory": c.find("implementationHistory").text,
                "channelDescription": c.find("channelDescription").text
                } for c in channel]

    return header,channels


def save_xml(data):
    tree = ET.parse(os.path.join(settings.BASE_DIR, r"ACQ\templates\ACQ\ModelACQ.XML"))
    root = tree.getroot()
    header = root.find("Header").findall("*")

    for node in nodes:
        for v,n in zip(data.POST.getlist(node),list(root.iter(node))):

            n.text = v
    header[1].text = data.user.username
    header[2].text = data.POST.get("inputShot")
    tree.write(get_file_link(data.POST.get("inputShot")))
def update_mds(data):
    new_data = []
    for node in mds_nodes:
        new_data.append(data.POST.getlist(node))
    
    new_data = np.asarray(new_data).T
    
    tree = MDSplus.Tree("exl50", 20000)
    for acqname,da in zip(data.POST.getlist("ChnlName"), new_data):
        for i in range(len(mds_nodes)):
            print("ACQ:"+acqname+":"+mds_nodes[i])
            n = tree.getNode("ACQ:"+acqname+":"+mds_nodes[i])
            n.deleteData()
            if mds_nodes[i]!="Unit":
                n.putData(float(da[i]))
            else:
                n.putData(da[i])
    tree.close()

