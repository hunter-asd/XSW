import xml.etree.cElementTree as et
from django.conf import settings
import os.path
import numpy as np
import MDSplus
from xml.dom import minidom
import uuid
import re
from xml_function import get_file_link
nodes = ['channelDescription', 'ChnlName', 'Unit', 'ChnlId', 'Len', 'Post', 'MaxDat', 'Freq', 'LowRang', 'HighRang', 'Factor', 'Offset', 'Dly', 'DatAttr', 'DatWth', 'division', 'personInCharge', 'fromPosition', 'insituPosition', 'implementationHistory']
mds_nodes=['Unit','LowRang', 'HighRang', 'Factor', 'Offset','MaxDat']


# 解析旧版的acq.xml,返回头信息和主内容
def parse_old_xml(shot):
    file = get_file_link("acq",shot)
    tree = et.parse(file)
    root = tree.getroot()
    return root.find("Header").findall("*"), root.findall("Channel")


# 将旧版的xml信息内容解析出来，转程字典列表格式
def load_old_xml(shot):
    header, channel = parse_old_xml(shot)
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

    return header, channels


# 生成保存xml文件，根据是否传入炮号来判别新旧
def save_xml(shot,data):
    if not shot:
        tree = et.parse(os.path.join(settings.BASE_DIR, r"acq\templates\acq\ModelACQ.XML"))
        root = tree.getroot()
        header = root.find("Header").findall("*")
        for node in nodes:
            for v,n in zip(data.POST.getlist(node), list(root.iter(node))):
                n.text = v
        header[1].text = data.user.username
        header[2].text = data.POST.get("inputShot")
        tree.write(get_file_link(data.POST.get("inputShot")))
    else:
        dom=minidom.parseString(data)
        dom.toprettyxml()
        with open(get_file_link("acq",shot), "w", encoding="UTF-8") as f:
            dom.writexml(f, indent='', addindent='\t', newl="\n", encoding='UTF-8')


# 将旧版acq.xml信息更新到MDSplus中
def update_mds(data):
    new_data = []
    for node in mds_nodes:
        new_data.append(data.POST.getlist(node))
    new_data = np.asarray(new_data).T
    tree = MDSplus.Tree("exl50", 20000)
    for acqname,da in zip(data.POST.getlist("ChnlName"), new_data):
        for i in range(len(mds_nodes)):
            print("acq:"+acqname+":"+mds_nodes[i])
            n = tree.getNode("acq:"+acqname+":"+mds_nodes[i])
            n.deleteData()
            if mds_nodes[i]!="Unit":
                n.putData(float(da[i]))
            else:
                n.putData(da[i])
    tree.close()


def update_dic(dic, k, v):
    if dic.get(k,None):
        if isinstance(dic[k], list):
            dic[k].append(v)
        else:
            dic[k] = list([dic[k], v])
    else:
        dic[k] = v


# list 转换成dic
def list_to_dic(k, lis):
    dic = {}
    for i in range(len(lis)):
        # dic[k+str(i+1)]=lis[i]
        dic[k+str(i+1)+"-"+list(lis[i].values())[0]] = lis[i]
    return dic


# 解析新版acq.xml文件，字典形式，多个节点则转换成字典列别：{node:[node1,node2...]}}
def parse_acq(root):
    dics = {}
    if root.getchildren():
        for n in root.getchildren():
            if n.getchildren():
                update_dic(dics, n.tag, parse_acq(n))
            else:
                dics[n.tag] = n.text
    else:
        dics[root.tag] = root.text
    return dics
# 解析出的xml数据转换成mind数据-node_tree
def xml_to_mind(d, xml):
    dics = {"id": d+"_"+str(uuid.uuid1().hex), "topic": d, "direction": "right", "expanded": True, "children": []}
    for k, i in zip(xml.keys(), range(len(xml))):
        if isinstance(xml[k], str):
            dics["children"]\
                .append({"id": k+"_"+str(uuid.uuid1().hex), "topic": k, "direction": "right", "expanded": True,
                    "children":[{"id": "strvalue_"+str(uuid.uuid1().hex), "topic": xml[k], "direction":"right",
                                 "expanded": True,"parent":k}]})
        elif isinstance(xml[k], dict):
            dics["children"].append(xml_to_mind(k, xml[k]))
        else:
            dics["children"].append(xml_to_mind(k, list_to_dic(k, xml[k])))
    return dics


def mind_to_xml(data):
    xml = ""
    if len(data["children"]) == 1 and not data["children"][0].get("children", None):
        return xml+"<{0}>{1}</{0}>".format(data["topic"], data["children"][0]["topic"])

    else:
        for child in data["children"]:
            xml += "\n" + mind_to_xml(child);
        if re.match("[A-Za-z]+",data["children"][0]["topic"]).group()==data["topic"]:
            return xml
        else:
            return "<{0}>\t\t{1}\n</{0}>".format(re.match("[A-Za-z]+", data["topic"]).group(), xml)


# 解析xml 成parameter格式和mind格式
def load_xml(shot):
    tree = et.parse(get_file_link("acq",shot))
    root = tree.getroot()
    param = parse_acq(root)
    b = xml_to_mind("acq", param)
    acqmind = {"meta":{"name":"ACQ_structural", "author": "liuyong", "version": "1"},
            "format":"node_tree","data":b}
    return param,str(acqmind).replace("\'", "\"").replace("True", "false")



