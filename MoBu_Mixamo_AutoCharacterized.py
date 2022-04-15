#
# MixamoモデルをTポーズにした後キャラクタライズするスクリプト
# python 3.7.7 
# MotionBuilder 2022

from pyfbsdk import *
import xml.etree.ElementTree as etree
import os
from pprint import pprint

def __GetSkeletonDefinitionDictionary() :
    """
    HIK.xmlを読み込んで「"定義ボーン名"："設定ボーン名"」のディクショナリにして返す関数
    """
    xmlFilePath = os.path.join(os.path.expanduser("~"), "Appdata", "Roaming", "Autodesk", "HIKCharacterizationTool6", "template", "HIK.xml")
    parsedXmlFile = etree.parse(xmlFilePath)
    skeletonDefinitionDictionary = {}
    for line in parsedXmlFile.iter("item"):
        jointName = line.attrib.get("value")
        if jointName:
            slotName = line.attrib.get("key")
            skeletonDefinitionDictionary[slotName] = jointName
    return skeletonDefinitionDictionary
    
def __FindJoint(jointName):
    joint = FBFindModelByLabelName(jointName)
    return joint     
       
def __ConvertTPose(skeletonDefinitionDictionary, characterName, namespace):
    for slotName, jointName in skeletonDefinitionDictionary.items():
        jointObj = __FindJoint(namespace + jointName)
        if jointObj :
            #Tスタンスにするためにローカル回転値をゼロクリア
            jointObj.SetVector( FBVector3d( 0, 0, 0 ), FBModelTransformationType.kModelRotation, False ) 

def Characterize(characterName, namespace):
    skeletonDefinitionDictionary = __GetSkeletonDefinitionDictionary()
    __ConvertTPose(skeletonDefinitionDictionary, characterName, namespace)
    #memo : ConvertTPoseを "character = FBCharacter(characterName)"より下で実行するとStatusに警告が出る
    character = FBCharacter(characterName)        
    for slotName, jointName in skeletonDefinitionDictionary.items():
        mappingSlot = character.PropertyList.Find(slotName + "Link")
        jointObj = __FindJoint(namespace + jointName)
        if jointObj :
            mappingSlot.append(jointObj)
    characterized = character.SetCharacterizeOn(True)
    if not characterized:
        pprint(character.GetCharacterizeError())
    else:
        FBApplication().CurrentCharacter = character

"""
Main
"""
Characterize("mixamo_character", "mixamorig:")
#Namespaceが無い場合
#Characterize("mixamo_character", "")

