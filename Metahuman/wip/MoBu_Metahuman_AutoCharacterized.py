# AポーズのMetahumanをTポーズにした後キャラクタライズするスクリプト
# python 3.7.7 
# MotionBuilder 2022

from pyfbsdk import *
import xml.etree.ElementTree as etree
import os
from pprint import pprint

class Rotation:
    x = 0.0
    y = 0.0
    z = 0.0

def GetSkeletonDefinitionDictionary(templateXmlFileName) :
    """
    SkeletonDefinitionXMLを読み込んで「"定義ジョイント名"："設定ジョイント名"」のディクショナリにして返す関数
    """
    xmlFilePath = os.path.join(os.path.expanduser("~"), "Appdata", "Roaming", "Autodesk", "HIKCharacterizationTool6", "template", templateXmlFileName)
    parsedXmlFile = etree.parse(xmlFilePath)
    skeletonDefinitionDictionary = {}
    for line in parsedXmlFile.iter("item"):
        jointName = line.attrib.get("value")
        if jointName:
            slotName = line.attrib.get("key")
            skeletonDefinitionDictionary[slotName] = jointName
    return skeletonDefinitionDictionary

def GetJoint(skeletonDefinitionDictionary, slotName):
    jointName = skeletonDefinitionDictionary.get(slotName)
    joint = FBFindModelByLabelName(jointName)
    return joint

def ImportXML(filePath):
    jointRotationDictionary = {}
    tree = etree.parse(filePath)
    root = tree.getroot()
    for joint in root.iter('joint'):
        rotation = Rotation()
        name = joint[0].text
        rotation.x = float(joint[1].text)
        rotation.y = float(joint[2].text)
        rotation.z = float(joint[3].text)
        jointRotationDictionary[name] = rotation
    return jointRotationDictionary
    
def FindJoint(jointName):
    joint = FBFindModelByLabelName(jointName)
    return joint     
       
def SetJointLocalRotation(jointName, x, y, z):
    joint = FindJoint(jointName)
    if joint:
        joint.SetVector( FBVector3d( x, y, z ), FBModelTransformationType.kModelRotation, False ) 

def Characterize(characterName, namespace):
    character = FBCharacter(characterName)
    skeletonDefinitionDictionary = GetSkeletonDefinitionDictionary("Metahuman.xml")
    for slotName, jointName in skeletonDefinitionDictionary.items():
        mappingSlot = character.PropertyList.Find(slotName + "Link")
        jointObj = FindJoint(namespace + jointName)
        if jointObj :
            mappingSlot.append(jointObj)
    characterized = character.SetCharacterizeOn(True)
    if not characterized:
        pprint(character.GetCharacterizeError())
    else:
        FBApplication().CurrentCharacter = character
    

def Execute():  
    pprint("call MoBu_Metahuman_Autocharacterized")
    #TPose変換 
    jointRotationDictionary = ImportXML("C:" + "\\ada.pose")
    for joint in jointRotationDictionary:
        rotation = jointRotationDictionary[joint]
        SetJointLocalRotation("ada:" + joint, rotation.x, rotation.y, rotation.z)
    #キャラクタライズ
    Characterize("ada_character", "ada:")

"""
Main
"""
Execute()
