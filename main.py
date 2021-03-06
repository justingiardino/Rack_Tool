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
#Not in production
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

#This function parses the dictionary and saves all data to a new xml file
def write_file_from_dict(dev_dict):
    #Element arguments (tag, attrib={})
    out_root = ET.Element('devices')
    #SubElement arguments (parent, tag, attrib={})
    for device in dev_dict:
        out_device = ET.SubElement(out_root, 'device', {'name':device})
        
        out_model = ET.SubElement(out_device,'model')
        out_model.text = dev_dict[device]['model']
        
        out_rack_u = ET.SubElement(out_device, 'rack_u')
        out_rack_u.text = dev_dict[device]['rack_u']
        
        out_rack_start = ET.SubElement(out_device, 'rack_start')
        out_rack_start.text = dev_dict[device]['rack_start']
        
        out_power = ET.SubElement(out_device, 'power')
        out_power.text = dev_dict[device]['power']
     
    #create xml string using ET
    xmlstr = ET.tostring(out_root).decode()
    #format xml string so it is not a flat file
    newxml = MD.parseString(xmlstr)
    
    #ask user for file name, maybe add an error check saying file needs to end in .xml
    out_name = input("Enter file name to save as(including .xml)\n>")
    #write data to file
    with open(out_name,'w') as outfile:
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
#returns True if there was enough room in the rack, False if there is no room
def build_rack(dev_dict):
    print('\n\nBuild Rack\n--------------------')
    #print(dev_dict) Nested dictionary
    #print(f"{dev_dict['RED-2920SW1']['model']}\n") Access single element

    #change later to a larger number
    rack_height = 10
    #format {rack start position:name}
    rack_full = {}
    for device in dev_dict:
        #check if rack is full at position where device is going
        #will need to add size check later
        #print(device)
        #print(f"Rack U's: {dev_dict[device]['rack_u']}")
        
        #check to see if height is one, or greater than one
        if dev_dict[device]['rack_u'] == '1':

            if dev_dict[device]['rack_start'] not in rack_full.keys():
                #print(dev_dict[device]['rack_start'])
                rack_full[dev_dict[device]['rack_start']] = device
                #else already full at that spot, need to error out
            else:
                print(f"Error, that spot at number {dev_dict[device]['rack_start']} is already taken by {rack_full[dev_dict[device]['rack_start']]}\nCannot place device {device} there!\n")
                return False
        #height not equal 1, may need to alter this later
        else:
            temp_u = dev_dict[device]['rack_u']
            temp_pos = dev_dict[device]['rack_start']
            temp_count = '1'
            #print(f"Rack height: {temp_u} and Rack start: {temp_pos}\nDifference: {int(temp_pos) - int(temp_u)}")
            #this loops through and adds a device to the rack multiple times when the height is larger than 1
            while True:
                #check if current position has already been filled
                if temp_pos not in rack_full.keys():
                    #add device to rack if not full
                    rack_full[temp_pos] = device
                    #move current position down one
                    temp_pos = str(int(temp_pos)-1)
                else:
                    print(f"Error, that spot at number {temp_pos} is already taken by {rack_full[temp_pos]}\nCannot place device {device} there!\n")
                    return False
                
                #check to see if the device has more U's that need to be added
                if temp_count != temp_u:
                    temp_count = str(int(temp_count)+1)
                    #print("More space needed")
                #if all U's of the device have been added leave this while loop
                elif temp_pos == '0':
                    print("Too low, cannot place device there")
                    return False
                elif temp_count == temp_u:
                    #print("Done adding device")
                    break
                else:
                    print("Rack full")#Why does this print rack full on first iteration?
                    return False
               
               #print("End of while loop")
                        
        #won't need this print in the end, this is for debugging
        #print(f"Count: {dev_dict[device]['count']}\nDevice: {device}\nModel: {dev_dict[device]['model']}\nPower: {dev_dict[device]['power']} Amps\nRack U: {dev_dict[device]['rack_u']}\nRack Start: {dev_dict[device]['rack_start']}\n")
    
    #This is where I will call GUI
    print(f"Contents of rack(Rack Position:Device Name): {rack_full}")
    
    return rack_full

def add_dev(dev_dict):
    #return old_dict if the device could not be added
    #old_dict = dev_dict
    print("Add Device\n------------")
    temp_name = input("Device Name\n>") #'RED-Sonitrol'#
    temp_model = input("Device Model\n>")#'Dell Optiplex 7010' #
    temp_rack_u = input("Device Height(Rack U's)\n>")#'1' #
    temp_start = input("Starting Rack Shelf\n>")#'9' #
    temp_power = input("Power Consumption(W)\n>")#'100' #
    
    #Need to find current count so I can increment
    curr_max = 0
    for device in dev_dict:
        temp_curr = int(dev_dict[device]['count'])
        if temp_curr > curr_max:
            curr_max = temp_curr
    
    #print(f"Current max value is {curr_max}")
    #increment count by one
    curr_max += 1
    
    #dev_dict.update(temp_name)
    #print(dev_dict['RED-2920SW1'])
    dev_dict[temp_name] = {}
    dev_dict[temp_name].update({'name':temp_name})
    dev_dict[temp_name].update({'model':temp_model})
    dev_dict[temp_name].update({'rack_u':temp_rack_u})
    dev_dict[temp_name].update({'rack_start':temp_start})
    dev_dict[temp_name].update({'power':temp_power})
    dev_dict[temp_name].update({'count':curr_max})
    
    
    print("Checking to see if this will fit in the rack.\n")
    if(build_rack(dev_dict)):
        print(f"\n\nNew information successfully added: {dev_dict[temp_name]}")
        #return updated dictionary to main if there was space
        return dev_dict
    
    else:
        print("Error, could not add device")
        #return false when device cannot be added
        return False
 
#This function removes a value from the dictionary
#Currently does not update count values. Not sure if I even need this value
def remove_dev(dev_dict):
    #create a temporary device list
    temp_list = []
    
    #print current devices on rack
    print("Current Devices:")
    for device in dev_dict:
        print(device)
        temp_list.append(device)
    print(temp_list)
    temp_dev = input("Which device would you like to remove?\n>")
    
    #check for valid entry, make sure that value is actually in the dictionary
    if temp_dev in temp_list:
        del dev_dict[temp_dev]
        print("Device Deleted")
        return dev_dict
    
    print('Error device is not in this rack.')
    return False

def print_rack(dev_dict):
    print("\n\nPrinting Device List\n------------------")
    for device in dev_dict:
        print(f"Count: {dev_dict[device]['count']}\nDevice: {device}\nModel: {dev_dict[device]['model']}\nPower: {dev_dict[device]['power']} Amps\nRack U: {dev_dict[device]['rack_u']}\nRack Start: {dev_dict[device]['rack_start']}\n")
    

#this function prints the current dictionary, just a place holder for now
#was used by the function save_vals_to_dict which is out of production
def print_dict(temp_dict):
    print(f"\nThis is device number {temp_dict['count']}\nName: {temp_dict['name']}\nRack U Height: {temp_dict['rack_u']}\nRack Start Location: {temp_dict['rack_start']}\nPower Usage: {temp_dict['power']}")


#main application menu, placeholder until GUI is in place
def main_menu():
    user_choice = 1
    print("\nWelcome to the Rack Builder!\n")
    while user_choice != '0':
        print("\nWhat would you like to do?\n1)View Existing Rack\n2)Add Device to Existing Rack\n3)Remove a Device from Existing Rack\n4)Build New Rack\n\nEnter 0 to exit")
        user_choice = input("> ")
        
        #1) View Existing Rack
        if user_choice == '1':
            print("What is the name of the file?")
            file_in = input("> ")#user input
            #file_in = 'device_out_new.xml'#auto entry
            main_root = open_file(file_in)
            main_dict = save_vals_to_nested_dict(main_root)
            #main_list has the indices where each device will be mounted on the rack
            main_list = build_rack(main_dict)
            print_rack(main_dict)
        #2) Add Device to Existing Rack
        elif user_choice == '2':
            print("What is the name of the file that has the rack you are adding to?")
            file_in = input("> ")#user input
            #file_in = 'device_list.xml'#auto entry
            main_root = open_file(file_in)
            main_dict = save_vals_to_nested_dict(main_root)
            new_main_dict = add_dev(main_dict)
            
            #check to see if dictionary changed, if not don't ask to save
            if new_main_dict:
                ask_save = input("Would you like to save this data to a file?\n1)Yes\n2)No\n>")
                if ask_save == '1':
                    print("Saving Data to File")
                    write_file_from_dict(new_main_dict)
                    
                #ask user if they want to see the new rack
                view_rack = input("Would you like to view the new rack?\n1)Yes\n2)No\n>")
                if view_rack == "1":
                    print_rack(new_main_dict)
         
        #3) Remove a Device from Existing Rack
        elif user_choice == '3':
            print("What is the name of the file that has the rack you are removing a device from?")
            file_in = input("> ")#user input
            #file_in = 'redding_w_cradlepoint.xml'#auto entry
            main_root = open_file(file_in)
            main_dict = save_vals_to_nested_dict(main_root)
            new_main_dict = remove_dev(main_dict)
            
            #check to see if dictionary changed, if not don't ask to save
            if new_main_dict:
                ask_save = input("Would you like to save this data to a file?\n1)Yes\n2)No\n>")
                if ask_save == '1':
                    print("Saving Data to File")
                    write_file_from_dict(new_main_dict)
                #ask user if they want to see the new rack
                view_rack = input("Would you like to view the new rack?\n1)Yes\n2)No\n>")
                if view_rack == "1":
                    print_rack(new_main_dict)    
                    
        
        #4) Build New Rack
        elif user_choice == '4':
            print('Not yet implemented')
            #new rack from scratch
        elif user_choice == '0':
            print('Good Bye!')
        else:
            print('Try again!')


if __name__ == '__main__':
    main_menu()