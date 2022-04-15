# MotionCaptureのプレビュー用に必要のないジョイント(補助骨)を削除するスクリプト
# python 3.7.7 
# MotionBuilder 2022

from pyfbsdk import *
import xml.etree.ElementTree as etree
import os
from pprint import pprint

def __GetSkeletonDefinitionList(templateXmlFileName) :
    """
    SkeletonDefinitionXMLを読み込んで「"定義ジョイント名"："設定ジョイント名"」のディクショナリにして返す関数
    """
    xmlFilePath = os.path.join(os.path.expanduser("~"), "Appdata", "Roaming", "Autodesk", "HIKCharacterizationTool6", "template", templateXmlFileName)
    parsedXmlFile = etree.parse(xmlFilePath)
    skeletonDefinitionList = []
    for line in parsedXmlFile.iter("item"):
        jointName = line.attrib.get("value")
        if jointName:
            skeletonDefinitionList.append(jointName)
    return skeletonDefinitionList

def __Delete(jointName):
    jointObj = FBFindModelByLabelName(jointName)
    if jointObj:
        jointObj.FBDelete()

def JointReduction(namespace):
    """
    選択中のジョイントからMetahuman.xmlに定義されていないジョイントを削除する
    """
    skeletonDefinitionList = __GetSkeletonDefinitionList("Metahuman.xml")
    selects = FBModelList()
    FBGetSelectedModels(selects) 
    selectJoints = [select.Name.replace(namespace,'') for select in selects]
    jointReductionList = list(set(selectJoints) - set(skeletonDefinitionList))
    pprint(jointReductionList)
    pprint("delete " + str(len(jointReductionList)) + " joints")    
    for joint in jointReductionList:
        __Delete(namespace + joint)

"""
Main
"""
JointReduction("ada:")
#Namespaceが無い場合
#JointReduction("")