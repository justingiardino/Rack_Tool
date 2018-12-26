#!/usr/bin/env python3

#xml format
#<tag attribute=value>text</tag>

#ET used for most xml manipulation
#MD used to format the xml file
import xml.etree.ElementTree as ET
import xml.dom.minidom as MD


#This function opens the provided file and finds the "root" of the XML tree
#Improvements: ask for filename? Check if file exists?
def open_file(filename):
    #open and parse xml file, find root tag
    tree = ET.parse(filename)
    root = tree.getroot()
    #print_root(root)

    #format that root is returned as is only good when looping through entire tree
    #since this program will be accessing specific elements the dictionary was needed
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
#Issue right now is that the dictionary gets overwritten each time
#No longer in production
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
#This function stores the values of the xml file into a nested dictionary
def save_vals_to_nested_dict(root):
    dev_dict = {}
    #count is not part of the xml file, but may be helpful to know
    count = 0
    for elem in root:
        #add name to dictionary, first declare the nested dictionary
        dev_dict[elem.attrib['name']] = {}
        #then adds first entry to the nested dictionary
        dev_dict[elem.attrib['name']].update(elem.attrib)
        #loop through all elements and add them to the nested dictionary
        for subelem in elem:
            #dictionary entry with tag and text
            temp_dict = {subelem.tag:subelem.text}
            #add to end of nested dictionary
            dev_dict[elem.attrib['name']].update(temp_dict)
        count += 1
        #add count value to dictionary
        dev_dict[elem.attrib['name']].update({'count':count})
    #print(dev_dict)
    #print(f"RED2920 dictionary: {dev_dict['RED-2920SW1']}")
    return(dev_dict)

#this function will place all devices on the rack, checking to make sure there is space
#if there is no more space display an erorr and list the devices that collide
#put power calculation in another function
def build_rack(dev_dict):
    print('\n\nBuild Rack')
    #print(dev_dict) Nested dictionary
    #print(f"{dev_dict['RED-2920SW1']['model']}\n") Access single element

    #change later to a larger number
    rack_height = 10
    #format {rack start position:name}
    rack_full = {}
    for device in dev_dict:
        #check if rack is full at position where device is going
        #will need to add size check later
        if dev_dict[device]['rack_start'] not in rack_full.keys():
            #print(dev_dict[device]['rack_start'])
            rack_full[dev_dict[device]['rack_start']] = device
        #else already full at that spot, need to error out
        else:
            print(f"Error, that spot at number {dev_dict[device]['rack_start']} is already taken by {rack_full[dev_dict[device]['rack_start']]}\nCannot place device {device} there!\n")
            return
        #won't need this print in the end, this is for debugging
        print(f"Count: {dev_dict[device]['count']}\nDevice: {device}\nModel: {dev_dict[device]['model']}\nPower: {dev_dict[device]['power']} Amps\nRack U: {dev_dict[device]['rack_u']}\nRack Start: {dev_dict[device]['rack_start']}\n")

    print(rack_full)


#this function prints the current dictionary, just a place holder for now
#was used by the function save_vals_to_dict which is out of production
def print_dict(temp_dict):
    print(f"\nThis is device number {temp_dict['count']}\nName: {temp_dict['name']}\nRack U Height: {temp_dict['rack_u']}\nRack Start Location: {temp_dict['rack_start']}\nPower Usage: {temp_dict['power']}")

#main application menu, placeholder until GUI is in place
def main_menu():
    user_choice = 1
    print("\nWelcome to the Rack Builder!\n")
    while user_choice != '0':
        print("\nWhat would you like to do?\n1)View Existing Rack\n2)Add Device to Existing Rack\n3)Remove a Device from the Rack\n\nEnter 0 to exit")
        user_choice = input("> ")
        if user_choice == '1':
            print("What is the name of the file?")
            #file_in = input("> ")#user input
            file_in = 'device_list.xml'#auto entry
            main_root = open_file(file_in)
            main_dict = save_vals_to_nested_dict(main_root)
            build_rack(main_dict)
        elif user_choice == '2':
            print('Not yet implemented')
            #add message to end of this function asking to view rack after adding
            #add message to ask if you want to save this new design
        elif user_choice == '3':
            print('Not yet implemented')
            #add message to end of this function asking to view rack after adding
            #add message to ask if you want to save this new design
        elif user_choice == '0':
            print('Good Bye!')
        else:
            print('Try again!')


if __name__ == '__main__':
    main_menu()

    #open_file('device_out.xml')
