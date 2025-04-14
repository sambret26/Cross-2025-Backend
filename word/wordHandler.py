import xml.etree.ElementTree as ET
import zipfile
import shutil
import os

from constants import settings

def createWordFile(rewards):
    oldTextList = []
    newTextList = []
    for reward in rewards:
        category = reward[0]
        runner = reward[1]
        sex = runner.sex if runner.sex != "M" else "H"
        if runner.ranking != 0:
            oldTextList.append("R" + category + sex)
            newTextList.append(runner.ranking)
        if runner.last_name != "":
            oldTextList.append("L" + category + sex)
            newTextList.append(runner.last_name)
        if runner.first_name != "":
            oldTextList.append("F" + category + sex)
            newTextList.append(runner.first_name)
        if runner.time != "":
            time = getTimeValue(runner.time)
            oldTextList.append("T" + category + sex)
            newTextList.append(time)
    replaceTextInDocument(oldTextList, newTextList)

def replaceTextInDocument(oldTextList, newTextList):
    unzipDocx(settings.WORD_PATH + settings.EMPTY_WORD_FILENAME, settings.TEMP)
    xmlFilePath = os.path.join(settings.TEMP, 'word/document.xml')
    for oldText, newText in zip(oldTextList, newTextList):
        replaceFlagInXml(xmlFilePath, oldText, newText)
    zipDir(settings.TEMP, settings.WORD_PATH + settings.FINAL_WORD_FILENAME)
    shutil.rmtree(settings.TEMP)

def unzipDocx(docxPath, extractTo):
    with zipfile.ZipFile(docxPath, 'r') as zipRef:
        zipRef.extractall(extractTo)
        
def zipDir(directory, zipFile):
    with zipfile.ZipFile(zipFile, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                filePath = os.path.join(root, file)
                arcname = os.path.relpath(filePath, directory)
                zipf.write(filePath, arcname)
                
def replaceFlagInXml(filePath, flag, value):
    tree = ET.parse(filePath)
    root = tree.getroot()
    for elem in root.iter():
        if elem.text and flag in elem.text:
            elem.text = elem.text.replace(flag, str(value) if value != None else "")
    tree.write(filePath)

def getTimeValue(fullTime):
    time = fullTime
    if '.' in fullTime:
        time = fullTime.split(".")[0]
    if time.startswith("00:"):
        time = time[3:]
    return time