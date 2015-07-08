__author__ = 'gnt'

import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

class parser():
    def __init__(self):
        self.tree = ET.parse('fr.xliff')
        self.root = self.tree.getroot()
        self.ns = {"target": ".//{urn:oasis:names:tc:xliff:document:1.2}target",
                   "trans-unit":".//{urn:oasis:names:tc:xliff:document:1.2}trans-unit",
                   "file":".//{urn:oasis:names:tc:xliff:document:1.2}file"}

    def returnLocalizableStrings(self):
        strings = []
        for transUnit in self.root.findall(self.ns['trans-unit']):
            if(len(transUnit)>1):
                string = []
                string.append(transUnit[0].text)
                try:
                    string.append(transUnit[1].text)
                except:
                    string.append("")
                try:
                    string.append(transUnit[2].text)
                except:
                    string.append("no comment")
                string.append(transUnit.attrib['id'])
                strings.append(string)
        return strings

    #return the source-language ISO639 code of the first <file> of the xliff
    def getSourceLanguage(self):
        return self.root.find(self.ns['file']).attrib['source-language']

    def getTargetLanguage(self):
        return self.root.find(self.ns['file']).attrib['target-language']

    def translate(self, translation, transID):
        transUnits = self.root.findall(self.ns['trans-unit'])
        for unit in transUnits:
            if unit.attrib['id'] == transID:
                print("found")
                unit[1].text = translation

    def saveIOS(self, name):
        self.tree.write(name +".xliff")

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

    def prettify(self, elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        print(reparsed.toprettyxml(indent="\t"))
        return reparsed.toprettyxml(indent="\t")




