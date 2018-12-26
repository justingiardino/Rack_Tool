#!/usr/bin/env python3

#xml format
# <tag attribute=value>text</tag>

#ET used for most xml manipulation
#MD used to format the xml file
import xml.etree.ElementTree as ET
import xml.dom.minidom as MD

#open and parse xml file, find root tag
tree = ET.parse('device_list.xml')
root = tree.getroot()

# all items data
print('\nAll item data:')
elem_num = 1
for elem in root:
    #elem is each device tag
    #attrib is a dictionary with 'name' as the key and actual device name as the value
    #printing elem.tag will display the word device
    print(f"\nDevice #: {elem_num}, {elem.attrib['name']}")
    elem_num += 1
    for subelem in elem:
        print(f"{subelem.tag} = {subelem.text}")


#output to an xml file
#Element arguments (tag, attrib={})
out_root = ET.Element('devices')
#SubElement arguments (parent, tag, attrib={})
out_device = ET.SubElement(out_root, 'device', {'name':'WIL-2920SW1'})
out_model = ET.SubElement(out_device, 'model')
#add text to tag
out_model.text = 'HP 2920'
out_rack_u = ET.SubElement(out_device, 'rack_u')
out_rack_u.text = '1'
out_rack_start = ET.SubElement(out_device, 'rack_start')
out_rack_start.text = '12'
out_power = ET.SubElement(out_device, 'power')
out_power.text = '200'


#create xml string using ET
xmlstr = ET.tostring(out_root).decode()
#format xml string so it is not a flat file
newxml = MD.parseString(xmlstr)
#write data to file
with open('device_out.xml','w') as outfile:
    outfile.write(newxml.toprettyxml(indent='\t',newl='\n'))
    
print("\nFile output complete!")

