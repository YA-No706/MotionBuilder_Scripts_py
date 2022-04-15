#
# Tポーズキャラクターの各ジョイントのローテーションを書き込んだファイルを出力するスクリプト
# python 3.7.7 
# MotionBuilder 2022
#
from pyfbsdk import *
from pyfbsdk_additions import *
import xml.etree.ElementTree as etree
import xml.dom.minidom
import os
from pprint import pprint

def GetSkeletonDictionary(templateXmlFileName) :
    """
    SkeletonDefinitionXMLを読み込んで「"設定ジョイント名" : ""」のディクショナリにして返す関数
    """
    xmlFilePath = os.path.join(os.path.expanduser("~"), "Appdata", "Roaming", "Autodesk", "HIKCharacterizationTool6", "template", templateXmlFileName)
    parsedXmlFile = etree.parse(xmlFilePath)
    skeletonDictionary = {}
    for line in parsedXmlFile.iter("item"):
        jointName = line.attrib.get("value")
        if jointName:
            skeletonDictionary[jointName] = ""
    return skeletonDictionary

def FindJoint(jointName):
    joint = FBFindModelByLabelName(jointName)
    return joint

#return localRotation[0] = X, localRotation[1] = y, localRotation[2] = z
def GetJointLocalRotation(jointName):
    joint = FindJoint(jointName)
    localRotation = FBVector3d()
    joint.GetVector(localRotation, FBModelTransformationType.kModelRotation, False)
    return localRotation

def ExportXML(exportPath, characterName, namespace, skeletonDictionary):
    #XML文字列の生成
    root = etree.Element('root', {'CharacterName':characterName})
    p = etree.SubElement(root, 'description') 
    t = etree.SubElement(p, 'Rotation_order') 
    t.text = 'Euler XYZ'
    p = etree.SubElement(root, 'joints') 
    for jointName in skeletonDictionary:
        t = etree.SubElement(p, 'joint')
        name = etree.SubElement(t, 'name')
        name.text = jointName
        rot = GetJointLocalRotation(namespace + jointName)
        x =  etree.SubElement(t, 'rot_x')
        x.text = str(rot[0])
        y =  etree.SubElement(t, 'rot_y')
        y.text = str(rot[1])
        z =  etree.SubElement(t, 'rot_z')
        z.text = str(rot[2])        
    #XMLファイルの生成
    dom = xml.dom.minidom.parseString(etree.tostring(root, 'utf-8'))
    fileName = characterName + '.pose' 
    file = open(exportPath + fileName, 'w')
    dom.writexml(file, encoding='utf-8', newl= '\n', indent='', addindent='    ')
    file.close()    
    FBMessageBox("Export Pose File", "Export to " + exportPath + fileName, "OK", None, None)
   
def Execute():
    pprint("call Mobu_Export_PoseAsset")
    #マッピングされているジョイントを取得 TODO : ここファイルからじゃなくシーンから取得するように修正　選択中のジョイントでよさそう
    dictionary = GetSkeletonDictionary("Metahuman.xml")
    ExportXML("C:\\", 'ada', 'ada:', dictionary)
