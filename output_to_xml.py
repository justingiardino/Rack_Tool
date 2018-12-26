#!/usr/bin/env python3

#xml format
#<tag attribute=value>text</tag>

#ET used for most xml manipulation
#MD used to format the xml file
import xml.etree.ElementTree as ET
import xml.dom.minidom as MD


#output to an xml file
#Element arguments (tag, attrib={})
a = ET.Element('a')
#SubElement arguments (parent, tag, attrib={})
b = ET.SubElement(a, 'b', {'tag_b':'attrib_b'})
b.text = 'text_b'
c = ET.SubElement(a, 'c')
d = ET.SubElement(c, 'd')
xmlstr = ET.tostring(a).decode()
#newxml = MD.parse(xmlstr)
newxml = MD.parseString(xmlstr)
with open('test.xml','w') as outfile:
    outfile.write(newxml.toprettyxml(indent='\t',newl='\n'))
    
