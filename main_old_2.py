#!/usr/bin/env python3

#xml format
#<tag attribute=value>text</tag>

#ET used for most xml manipulation
#MD used to format the xml file
import xml.etree.ElementTree as ET
import xml.dom.minidom as MD
print("Welcome to the Rack Builder!\n")


#This function opens the provided file and finds the "root" of the XML tree
#Improvements: ask for filename? Check if file exists?
def open_file(filename):
    #open and parse xml file, find root tag
    tree = ET.parse(filename)
    root = tree.getroot()
    #print_root(root)  
    #use root later in program
    return root

#This function scans through the XML tree and prints all tags and text
#Mostly use for error/sanity checks    
def print_root(root):
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

#This function writes an XML string out to a file
#Currently is manually adding elements, need to make this dynamic            
def write_file():
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


#This function creates a dictionary for each device, 
#Issue right now is that the dictionary gets overwritten each time through for now
#Look into nested dict https://stackoverflow.com/questions/16333296/how-do-you-create-nested-dict-in-python
#Maybe make this a class?
def save_vals_to_dict(root):
    dev_dict = {}
    #count is not part of the xml file, but may be helpful to know
    count = 0
    for elem in root:
        #add name to dictionary
        dev_dict.update(elem.attrib)
        #loop through all elements and add them to the device dictionary
        for subelem in elem:
            #dictionary entry with tag and text
            temp_dict = {subelem.tag:subelem.text}
            dev_dict.update(temp_dict)
        count += 1
        #add count value to dictionary
        dev_dict.update({'count':count})
        #display current dictionary before it gets overwritten
        print_dict(dev_dict)

#using nested dictionary, not yet added to production code
def save_vals_to_nested_dict(root):
    dev_dict = {}
    #count is not part of the xml file, but may be helpful to know
    count = 0
    for elem in root:
        #add name to dictionary
        dev_dict[elem.attrib['name']] = {}
        dev_dict[elem.attrib['name']].update(elem.attrib)
        #loop through all elements and add them to the device dictionary
        for subelem in elem:
            #dictionary entry with tag and text
            temp_dict = {subelem.tag:subelem.text}
            dev_dict[elem.attrib['name']].update(temp_dict)
        count += 1
        #add count value to dictionary
        dev_dict[elem.attrib['name']].update({'count':count})
        #display current dictionary before it gets overwritten
        print(dev_dict)

#this function prints the current dictionary, just a place holder for now
def print_dict(temp_dict):
    print(f"\nThis is device number {temp_dict['count']}\nName: {temp_dict['name']}\nRack U Height: {temp_dict['rack_u']}\nRack Start Location: {temp_dict['rack_start']}\nPower Usage: {temp_dict['power']}")

#maybe make this a class?
def build_rack(temp_dict):
    print("Building out rack.")
    

def main_menu():
    user_choice = 1
    while user_choice != '0':
        print("\n\nWhat would you like to do?\n1)View Existing Rack\n2)Add Device to Existing Rack\n3)Remove a Device from the Rack\n\nEnter 0 to exit")
        user_choice = input("> ")
        if user_choice == '1':
            print("What is the name of the file?")
            file_in = input("> ")
            main_root = open_file(file_in)
            save_vals_to_dict(main_root)
            #save_vals_to_nested_dict(main_root)
        elif user_choice == '2':
            print('Not yet implemented')
        elif user_choice == '3':
            print('Not yet implemented')
        elif user_choice == '0':
            print('Good Bye!')
        else:
            print('Try again!')
            

if __name__ == '__main__':   
    main_menu()
    #main_root = open_file('device_list.xml')#maybe have this do a windows file chooser?
    #save_vals_to_dict(main_root)
    #write_file()
    #open_file('device_out.xml')