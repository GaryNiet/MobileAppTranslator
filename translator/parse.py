__author__ = 'gnt'

import xml.etree.ElementTree as ET
import re


class parser():
    def __init__(self):
        self.values = []
        file = open("file.strings", 'r')
        strings = []
        for line in file:
            value = line.split("\"")
            self.values.append([value[1],value[3]])
        file.close()


    def returnLocalizableStrings(self):
        strings = []
        for value in self.values:
            print("prout")
            string = []
            string.append(value[0])
            string.append(value[1])
            string.append("comment")

            strings.append(string)
        return strings

    #return the source-language ISO639 code of the first <file> of the xliff
    def getSourceLanguage(self):
        return "en"

    def getTargetLanguage(self):
        return "fr"

    def translate(self, translation, transID):
        self.values[transID][1] = translation

    def saveIOS(self, name):
        print(self.values)

    def saveAndroid(self,name):

        xmlFileRoot = ET.Element('resources')
        transUnits = self.root.findall(self.ns['trans-unit'])
        for unit in transUnits:
            try:
                string = ET.Element('string')
                string.text = unit[0].text
                string.set('name',unit.attrib['id'])
                xmlFileRoot.append(string)
            except:
                pass
        f = open(name +'.xml', 'w')
        f.write(self.prettify(xmlFileRoot))





    def changeLanguage(self, newLanguageCode):
        array = self.root.findall(self.ns['file'])
        for files in array:
            files.attrib['target-language'] = newLanguageCode






