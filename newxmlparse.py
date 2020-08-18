import xml.etree.cElementTree as et
import random
import uuid

#更新字典，如果键值不存在于字典，就加入键值对，如果已经存在，但值是列表，就更新对应列表，如果不是列表就将键值和新值更新为列表
def updateDic(dic, k, v):
    if dic.get(k, None):
        if isinstance(dic[k], list):
            dic[k].append(v)
        else:
            dic[k] = list([dic[k], v])
    else:
        dic[k] = v

def listtoDic(k,lis):
    dic={}
    for i in range(len(lis)):
        dic[k+str(i+1)]=lis[i]
    return dic

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

def xmltomind(d,xml):
    # if not dicindic(xml):
    #     return {"id": d, "topic": d, "direction": "right", "expanded": True,"children":minddata(xml)}
    # else:

    dics={"id": d+"_"+str(uuid.uuid1().hex), "topic": d, "direction": "right", "expanded": True,"children":[]}
    for k,i in zip(xml.keys(),range(len(xml))):
        if isinstance(xml[k], str):
            dics["children"].append({"id": k+"_"+str(uuid.uuid1().hex), "topic": k+":"+xml[k], "direction": "right", "expanded": True})
        elif isinstance(xml[k], dict):
            dics["children"].append(xmltomind(k,xml[k]))
        else :
            dics["children"].append(xmltomind(k,listtoDic(k,xml[k])))
    return dics

def parseNewAcq(path):
    tree = et.parse(r"C:\Users\liuyongag\Desktop\NewVersionAcq.XML")
    root = tree.getroot()
    param = findAllXmlNodes(root)
    b = xmltomind("acq", param)
    acqmind=mid={"meta":{"name":"ACQ_structural","author":"liuyong","version":"2"},
"format":"node_tree","data":b}

    return param,acqmind
if __name__ =="__main__":
    tree = et.parse(r"C:\Users\liuyongag\Desktop\NewVersionAcq.XML")
    root = tree.getroot()
    a=findAllXmlNodes(root)
    b=xmltomind("acq",a)
    mid={"meta":{"name":"jsMind remote","author":"hizzgdev@163.com","version":"0.2"},
"format":"node_tree","data":b}
    with open(r"C:\Users\liuyongag\Desktop\NewVersionAcq.jm","w") as f:
        f.write(str(mid).replace("\'","\"").replace("True","false"))