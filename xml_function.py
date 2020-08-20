import xml.etree.cElementTree as et
import uuid
import os.path
import re
import numpy as np
import xml.dom.minidom as mdm
from functools import reduce
from django.conf import  settings

#更新字典，如果键值不存在于字典，就加入键值对，如果已经存在，但值是列表，就更新对应列表，如果不是列表就将键值和新值更新为列表
def update_dic(dic, k, v):
    if dic.get(k, None):
        if isinstance(dic[k], list):
            dic[k].append(v)
        else:
            dic[k] = list([dic[k], v])
    else:
        dic[k] = v

#递归解析XML文件{"节点":{"子节点":"值"},"节点":[{"子节点":"值"},...],"节点":"值"}
def parse_xml(root):
    params_dic = {}
    if root.getchildren():
        for n in root.getchildren():
            if n.getchildren():
                update_dic(params_dic, n.tag, parse_xml(n))
            else:
                params_dic[n.tag] = n.text
    else:
        params_dic[root.tag] = root.text
    return params_dic

#列表转换为字典
def list_to_dic(k, lis):
    dic = {}
    for i in range(len(lis)):
        # dic[k+str(i+1)]=lis[i]
        dic[k+str(i+1)+"-"+list(lis[i].values())[0]] = lis[i]
    return dic

#xml字典数据转换为mind数据格式
def xml_to_mind(top, xml_data_dic):
    dics = {"id": top + "_" + str(uuid.uuid1().hex), "topic": top, "direction": "right", "expanded": True, "children": []}
    for k, i in zip(xml_data_dic.keys(), range(len(xml_data_dic))):
        if isinstance(xml_data_dic[k], str):
            dics["children"]\
                .append({"id": k+"_"+str(uuid.uuid1().hex), "topic": k, "direction": "right", "expanded": True,
                    "children":[{"id": "strvalue_"+str(uuid.uuid1().hex), "topic": xml_data_dic[k], "direction": "right",
                                 "expanded": True,"parent":k}]})
        elif isinstance(xml_data_dic[k], dict):
            dics["children"].append(xml_to_mind(k, xml_data_dic[k]))
        else:
            dics["children"].append(xml_to_mind(k, list_to_dic(k, xml_data_dic[k])))
    return dics
#mind格式数据转换成xml数据
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
# 生成mind 数据文件
def gen_mind_file(xmltype,xmlpath,mindpath):
    tree = et.parse(xmlpath)
    root = tree.getroot()
    xml_dics = parse_xml(root)
    mind_data = xml_to_mind(xmltype,xml_dics)
    main_data = {"meta": {"name": "jsMind ", "author": "hizzgdev@163.com", "version": "0.2"}, "format": "node_tree",
                 "data": mind_data}
    with open(mindpath, "w") as f:
        f.write(str(main_data).replace("\'", "\"").replace("True", "false"))

#美化，格式化xml
def pretty_xml(element, indent, newline, level = 0): # elemnt为传进来的Elment类，参数indent用于缩进，newline用于换行
    if element:  # 判断element是否有子元素
        if element.text == None or element.text.isspace(): # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
    #else:  # 此处两行如果把注释去掉，Element的text也会另起一行
    #element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element) # 将elemnt转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1): # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        pretty_xml(subelement, indent, newline, level = level + 1) # 对子元素进行递归操作
    return element

#filetype :acq/dpf/tcn
def get_file_link(filetype,shot):
    filename=filetype
    if filetype=="TCN":
        filename="OUT"
    path = settings.XMLPATH
    folder = ("00000"+str(int(shot)//200*200))[-5:]
    link = os.path.join(path, folder, filetype, ("00000"+str(shot))[-5:]+filename+".xml")
    return link

def load_xml(shot,type):
    file_path = get_file_link(type,shot)
    root = et.parse(file_path).getroot()
    return parse_xml(root)


def save_xml(xmltype,submit_dic):
    submit_dic.pop("csrfmiddlewaretoken")
    shot = submit_dic.pop("input-shot")
    data=[]
    for v in submit_dic:
        data.append(v)
    data=np.array(data).T







if __name__=="__main__":

    gen_mind_file("ACQ",r"C:\Users\liuyongag\Desktop\NewXml\NewVersionAcq.XML", r"C:\Users\liuyongag\Desktop\NewXml\NewVersionAcq.jm")
