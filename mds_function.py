import MDSplus
import datetime
import xml.etree.cElementTree as et
import os.path
from django.conf import  settings


def get_current_shot(target="MDS"):
    if target == "MDS":
        try:
            return MDSplus.Tree.getCurrent("EXL50")
        except Exception as e:
            get_current_shot()
    else:
        tree = et.parse(os.path.join(settings.XMLPATH), r"CurrentShotNum\CurrentShotNum.xml")
        root = tree.getroot()
        return int(root.iter("shotnum").__next__().text)


def get_exp_time(shot):
    tree = MDSplus.Tree("EXL50", shot)
    time = datetime.datetime.utcfromtimestamp(tree.getNode("fbc:ip").getTimeInserted().time).strftime("%Y.%m.%d %H:%M:%S")
    tree.close()
    return time


def get_ip_max_value(shot):
    tree = MDSplus.Tree("EXL50", shot)
    tree.setTimeContext(0, 6, None)
    mvalue = str(round(tree.getNode("fbc:ip").data().max(), 2))
    tree.setTimeContext(None, None, None)
    tree.close()
    return mvalue


def find_effective_shot(shot):
    tree = MDSplus.Tree("EXL50", shot)
    n = tree.getNode("fbc:ip")
    try:       
        n.data()
        return shot
    except MDSplus.mdsExceptions.TreeNODATA:
        return find_effective_shot(shot - 1)


def get_effective_newest_shot(target="MDS"):
    shot = get_current_shot(target)
    return find_effective_shot(shot)

#filetype :acq/dpf/tcn
def get_file_link(filetype,shot):
    filename=filetype
    if filetype=="tcn":
        filename="OUT"
    path = settings.XMLPATH
    folder = ("00000"+str(int(shot)//200*200))[-5:]
    link = os.path.join(path, folder, filetype, ("00000"+str(shot))[-5:]+filename+".xml")
    return link
