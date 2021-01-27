import MDSplus
import datetime
import xml.etree.cElementTree as et
import os.path
import numpy as np
from django.conf import  settings


#获取当前炮号，一种途径是从mds数据库获取，一种是本地xml文件获取，默认是XML文件获取
def get_current_shot(target="XML",path="192.168.20.11::media/ennfusion/trees/exl50"):
    """
    :param target: 获取途径
    :param path: mds数据库remote路径
    :return: int 炮号
    """
    if target == "MDS":
        try:
            return MDSplus.Tree.getCurrent("EXL50",path=path)
        except Exception as e:
            return get_current_shot()
    else:
        print("asd")
        tree = et.parse(os.path.join(settings.XMLPATH, r"CurrentShotNum\CurrentShotNum.xml"))
        root = tree.getroot()
        return int(root.iter("shotnum").__next__().text)

#获取最近的有效的炮数据，包括炮号，实验时间，ip电流最大值
def get_effective_shot_data(target="xml",times=3,path="192.168.20.11::media/ennfusion/trees/exl50"):
    """
    :param target: 当前炮号获取途径
    :param times: 向后寻找的次数
    :param path: mdsplus数据库远程路径
    :return: int current_shot -当前炮号 str exp_time -实验时间 str mvalue -ip最大值
    """
    current_shot = get_current_shot(target=target)
    ipdata=np.array([])
    while times:
        tree = MDSplus.Tree("EXL50", current_shot, path=path)
        tree.setTimeContext(0, 6, None)
        node = tree.getNode("fbc:ip")
        try:
            ipdata=node.data()
            break
        except MDSplus.mdsExceptions.TreeNODATA:
            times-=1
            current_shot-=1
            tree.close()

    if ipdata.size!=0.:
        exp_time = datetime.datetime.utcfromtimestamp(tree.getNode("fbc:ip").getTimeInserted().time).strftime(
            "%Y.%m.%d %H:%M:%S")
        try:
            mvalue = str(round(tree.getNode("fbc:ip").data().max(), 2))
        except Exception as e:
            mvalue = "NA"
        tree.setTimeContext(None, None, None)
        tree.close()
    else:
        exp_time="NA"
        mvalue="NA"


    return current_shot,exp_time,mvalue



