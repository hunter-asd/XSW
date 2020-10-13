import xml.etree.cElementTree as et
import uuid
import os.path
import re
import numpy as np
from xml.dom import minidom
from lxml import etree as  let
from django.conf import  settings
import mds_function
import copy
HEADER=r"<Header><version>2.0</version><operator>{}</operator><shotnum>{}</shotnum></Header>"

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
    if filetype.upper()=="TCN":
        filename="OUT"
    path = settings.XMLPATH
    folder = ("00000"+str(int(shot)//200*200))[-5:]
    link = os.path.join(path, folder, filetype, ("00000"+str(shot))[-5:]+filename+".xml")
    return link

def load_xml(shot,type):
    file_path = get_file_link(type,shot)
    root = et.parse(file_path).getroot()
    return parse_xml(root)



#构造element 子节点
def build_element_instance(keys):
    n_set=set()
    for k in keys:
        n_set.update(k.split("_"))
    nodes={}
    multi_nodes={}
    for n in n_set:
        nodes[n]=et.Element(n)
        multi_nodes[n] = et.Element(remove_tail_digit(n))
    return nodes,multi_nodes

def append_tag(parent,son,nodes,multi_nodes=None):

    if nodes[parent].find(nodes[son].tag) !=None:
        pass
    else:
        if multi_nodes:
            multi_nodes[parent].append(multi_nodes[son])
            nodes[parent].append(nodes[son])
        else:
            nodes[parent].append(nodes[son])
#移除字符串末尾的数字
def remove_tail_digit(a):
    if a[-1].isdigit():
        return remove_tail_digit(a[:-1])
    else:
        return a
def save_tcn(data,user):
    data.pop("csrfmiddlewaretoken")
    shot = "00000"+data.pop("input-shot")[0]
    shot=shot[-5:]
    keys = data.keys()
    values = np.array(list(data.values())).T
    print(len(keys),values.shape)
    # 将数据按照行信号，列节点组织数据
    header = et.fromstring(HEADER.format(user,shot))
    #构建包含命名空间的根节点
    tcn_etree=et.ElementTree(et.fromstring("""<timingOutputSignal xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xsi:noNamespaceSchemaLocation="timingOutputSignals.xsd"></timingOutputSignal>"""))
    tcn_root = tcn_etree.getroot()
    tcn_root.append(header)
    # 按照信号来循环处理
    for i in range(len(values)):
        # 生成一个信号所有的节点
        nodes,multi_nodes = build_element_instance(keys)
        # 遍历一个信号的节点及节点值
        for k, v in zip(keys, values[i]):
            # 按节点路径来组织节点
            # 将节点路径解析成列表
            if v:
                k_list = k.split("_")
                for j in range(len(k_list) - 1):
                    append_tag(k_list[j], k_list[j + 1], nodes,multi_nodes)
                # 给最后一个节点赋值
                multi_nodes[k_list[-1]].text = v
        #outputSignal是二级节点
        tcn_root.append(multi_nodes["outputSignal"])
    dom = minidom.parseString(et.tostring(tcn_root))
    dom.toprettyxml()
    tcn_schema = let.XMLSchema(let.parse(r"tcn\templates\tcn\timingOutputSignals.xsd"))
    with open(get_file_link("TCN", shot), "w", encoding="UTF-8") as f:
        dom.writexml(f, indent='', addindent='\t', newl="\n", encoding='UTF-8')
    try:
        tcn_schema.assertValid(let.fromstring(et.tostring(tcn_root)))

        with open(get_file_link("TCN",shot), "w", encoding="UTF-8") as f:
            dom.writexml(f, indent='', addindent='\t', newl="\n", encoding='UTF-8')
        validation="success"
    except Exception as e:
        validation=e
    finally:
        return validation
#向列表添加不重复的元素
def unique_list(lst,value):
    try:
        lst.index(value)
    except ValueError :
        lst.append(value)
    return lst


def save_dpf(data,user):
    data.pop("csrfmiddlewaretoken")
    shot="00000"+data.pop("inputShot")[0]
    shot=shot[-5:]
    header = et.fromstring(HEADER.format(user, shot))
    dpf_tree=et.ElementTree(et.fromstring("""<DPF xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="DPF.xsd"></DPF>"""))
    dpf_root=dpf_tree.getroot()
    dpf_root.append(header)
    second=[]
    for k in data.keys():
        second=unique_list(second,k.split("_")[0])
    for s in second:
        s_group_v={}
        for k,v in data.items():
            if k.startswith(s):
                s_group_v[k]=v
        keys=s_group_v.keys()
        values=np.array(list(s_group_v.values())).T

        for v in values:
            if s == "OperationMode":
                print(v)
            #凡是空值或者值为None的节点，全部剔除掉
            if np.asarray(v == "", dtype=np.uint8).sum() != v.size:
                if np.asarray(v == "None", dtype=np.uint8).sum() != v.size:
                    nodes,_= build_element_instance(keys)
                    for key,value in zip(keys,v):
                        append_tag(key.split("_")[0],key.split("_")[1],nodes)
                        nodes[key.split("_")[1]].text=value
                    dpf_root.append(nodes[key.split("_")[0]])
    dom = minidom.parseString(et.tostring(dpf_root))
    dom.toprettyxml()
    dpf_schema = let.XMLSchema(let.parse(r"dpf\templates\dpf\DPF.xsd"))
    try:
        dpf_schema.assertValid(let.fromstring(et.tostring(dpf_root)))
        with open(get_file_link("DPF",shot), "w", encoding="UTF-8") as f:
            dom.writexml(f, indent='', addindent='\t', newl="\n", encoding='UTF-8')
        validation="success"
    except Exception as e:
        validation=e
    finally:
        return validation


def save_acq(data,user):
    data.pop("csrfmiddlewaretoken")
    shot = "00000"+data.pop("inputShot")[0]
    shot=shot[-5:]
    keys = data.keys()
    values = np.array(list(data.values())).T
    # 将数据按照行信号，列节点组织数据
    header = et.fromstring(HEADER.format(user,shot))
    #构建包含命名空间的根节点
    acq_etree=et.ElementTree(et.fromstring("""<ACQ xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="ACQ.xsd"></ACQ>"""))
    acq_root = acq_etree.getroot()
    acq_root.append(header)
    # 按照信号来循环处理
    for i in range(len(values)):
        # 生成一个信号所有的节点
        nodes,_ = build_element_instance(keys)
        # 遍历一个信号的节点及节点值
        if np.asarray(values[i] == "", dtype=np.uint8).sum() != values[i].size:
            if np.asarray(values[i] == "None", dtype=np.uint8).sum() != values[i].size:
                for k, v in zip(keys, values[i]):
                    # 按节点路径来组织节点
                    # 将节点路径解析成列表

                    k_list = k.split("_")
                    for j in range(len(k_list) - 1):
                        append_tag(k_list[j], k_list[j + 1], nodes)
                    # 给最后一个节点赋值
                    nodes[k_list[-1]].text = v

                acq_root.append(nodes["Channel"])
    dom = minidom.parseString(et.tostring(acq_root))

    dom.toprettyxml()
    tcn_schema = let.XMLSchema(let.parse(r"acq\templates\acq\ACQ.xsd"))
    try:
        tcn_schema.assertValid(let.fromstring(et.tostring(acq_root)))
        with open(get_file_link("acq",shot), "w", encoding="UTF-8") as f:
            dom.writexml(f, indent='', addindent='\t', newl="\n", encoding='UTF-8')
        validation="success"
    except Exception as e:
        validation = e
    finally:
        return validation




def add_node(node_name,shot,xml_type):
    xml_file = et.parse(get_file_link(xml_type,shot))
    xml_root =xml_file.getroot()
    new_node=copy.deepcopy(xml_root.find(node_name))
    for i in list(new_node):
        i.clear()
    xml_root.append(new_node)
    xml_file.write(get_file_link(xml_type,shot))

if __name__=="__main__":
    pass





