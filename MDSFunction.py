import MDSplus
import datetime
import xml.etree.cElementTree as et
import os.path
from django.conf import  settings
import uuid
def getCurrentShot(target="MDS"):
    if target=="MDS":
        return MDSplus.Tree.getCurrent("EXL50")
    else:
        tree = et.parse(os.path.join(settings.XMLPATH), r"CurrentShotNum\CurrentShotNum.xml")
        root = tree.getroot()
        return int(root.iter("shotnum").__next__().text)


def getExpTime(shot):
    tree = MDSplus.Tree("EXL50",shot)
    time = datetime.datetime.utcfromtimestamp(tree.getNode("fbc:ip").getTimeInserted().time).strftime("%Y.%m.%d %H:%M:%S")
    tree.close()
    return time
def getIpMaxValue(shot):
    tree = MDSplus.Tree("EXL50", shot)
    tree.setTimeContext(0, 6,None)
    mvalue = str(round(tree.getNode("fbc:ip").data().max(), 2))
    tree.setTimeContext(None, None, None)
    tree.close()
    return mvalue
def ifAndFindEffective(shot):
    tree=MDSplus.Tree("EXL50",shot)
    n=tree.getNode("fbc:ip")
    try:       
        data=n.data()
        return shot
    except MDSplus.mdsExceptions.TreeNODATA:
        return ifAndFindEffective(shot-1)

def getEffectiveCurrentShot(target="MDS"):
    
    if target=="MDS":
        shot = MDSplus.Tree.getCurrent("EXL50")

    else:
        tree = et.parse(os.path.join(settings.XMLPATH), r"CurrentShotNum\CurrentShotNum.xml")
        root = tree.getroot()
        shot = int(root.iter("shotnum").__next__().text)
    return ifAndFindEffective(shot)
def updateDic(dic,k,v):
    if dic.get(k,None):
        if isinstance(dic[k],list):
            dic[k].append(v)
        else:
            dic[k]=list([dic[k],v])
    else:
        dic[k]=v

#list 转换成dic
def listtoDic(k,lis):
    dic={}
    for i in range(len(lis)):
        dic[k+str(i+1)]=lis[i]
    return dic
#解析Newxml
def findAllXmlNodes(root):
    dics = {}
    if root.getchildren():
        for n in root.getchildren():
            if n.getchildren():
                updateDic(dics,n.tag,findAllXmlNodes(n))
            else:
                dics[n.tag] = n.text
    else:
        dics[root.tag] = root.text
    return dics
#解析出的xml数据转换成mind数据
def xmltomind(d,xml):

    dics={"id": d+"_"+str(uuid.uuid1().hex), "topic": d, "direction": "right", "expanded": True, "children":[]}
    for k, i in zip(xml.keys(), range(len(xml))):
        if isinstance(xml[k], str):
            dics["children"].append({"id": k+"_"+str(uuid.uuid1().hex), "topic": k, "direction": "right", "expanded": True,
                                     "children":[{"id": k+"str_"+str(uuid.uuid1().hex), "topic": xml[k], "direction": "right", "expanded": True,"parent":k}]})
        elif isinstance(xml[k], dict):
            dics["children"].append(xmltomind(k, xml[k]))
        else:
            dics["children"].append(xmltomind(k, listtoDic(k, xml[k])))
    return dics
#解析xml 成parameter格式和mind格式
def parseNewAcq(path):
    tree = et.parse(r"C:\Users\liuyongag\Desktop\NewXml\NewVersionAcq.XML")
    root = tree.getroot()
    param = findAllXmlNodes(root)
    print(param)
    b = xmltomind("Acq", param)
    acqmind={"meta":{"name":"ACQ_structural","author":"liuyong","version":"2"},
"format":"node_tree","data":b}
    return param,str(acqmind).replace("\'","\"").replace("True","false")
