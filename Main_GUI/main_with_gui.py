#!/usr/bin/env python3

#todo: Option to edit device on rack
#Add quit feature
#Move Rack number to be its own widget
#open file to last location in Explorer/Finder
#when saving new file you have to actually type xml, why?
#drag and drop box
#UPS support
#count bug?

#change menu structure
#This will cut down on the opening of files and confusion with display
#File > Open New Rack
#File > Create New Rack
#File > Save Current Rack(Should open to current directory)
#File > Quit(Warn before quiting)
#Edit > Add device to rack (current file, don't open new)
#Edit > Remove Device from Rack
#Edit > Edit Device on Rack (Change name, model, power, or location)
#View > Rack vs Power?

#perfect time to create new class for current rack

#xml format
#<tag attribute=value>text</tag>

#ET used for most xml manipulation
#MD used to format the xml file
#PyQt5 used for GUI

import sys
import xml.etree.ElementTree as ET
import xml.dom.minidom as MD
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QApplication, QAction, QFileDialog, QInputDialog, QMessageBox, QGridLayout, QVBoxLayout, QGroupBox, QLabel, QWidget, QStyleFactory, QToolTip, qApp
#from PyQt5.QtGui import QPainter, QBrush
#from PyQt5.QtCore import Qt

class DisplayMain(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Main Window'
        self.left = 100
        self.top = 100
        self.width = 500
        self.height = 150
        self.maxRackHeight = 20
        #creating rack objects
        self.curr_rack = Rack()
        self.new_rack = Rack()
        self.initUI()

    def initUI(self):
        #create a statusBar for display later
        self.statusBar()

        menubar = self.menuBar()

        fileMenu =  menubar.addMenu('File')
        editMenu = menubar.addMenu('Edit')

        #Create Actions
        viewAct = QAction('View Existing Rack', self)
        newAct = QAction('Add Device to Rack', self)
        remAct = QAction('Remove Device from Rack', self)
        quitAct = QAction('Quit', self)

        #connect actions to functions
        viewAct.triggered.connect(self.viewRack)
        newAct.triggered.connect(self.addToRack)
        remAct.triggered.connect(self.removeFromRack)
        quitAct.triggered.connect(self.quitProgram)

        #add actions to file menu
        fileMenu.addAction(viewAct)
        fileMenu.addAction(quitAct)

        #add actions to edit menu
        editMenu.addAction(newAct)
        editMenu.addAction(remAct)

        #create grid for display
        self.createGridLayout()
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        #make this the central widget of the main menu
        self.setCentralWidget(self.horizontalGroupBox)

        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.show()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Rack")
        self.layout = QGridLayout()
        self.layout.setColumnStretch(0, self.width / 2)
        self.layout.setColumnStretch(1, self.width / 2)

        #layout idea - column 0 = number, really small column width
        #column 1 = Device name with tool tip
        for i in range(self.maxRackHeight):
            for j in range(2):
                if j == 0:
                    label = QLabel(str(self.maxRackHeight - i))
                    #label.setFrameStyle(QFrame.Box)
                    label.setStyleSheet("QLabel { background-color : silver; color : black; }")
                    #self.layout.addWidget(QLabel(str(self.maxRackHeight - i)), i, j)
                    self.layout.addWidget(label, i, j)
                else:
                    self.layout.addWidget(QLabel(""), i, j)
                #print(self.layout.itemAtPosition(i,j))

        self.horizontalGroupBox.setLayout(self.layout)

    def clearGridLayout(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

    #keep j in range loop because later there will be more columns
    def printRack_GUI(self, rack_pos_dict, main_dict):
        for i in range(self.maxRackHeight):
            for j in range(2):
                #need to add j = 1 logic later

                if j == 0:
                    if str(self.maxRackHeight - i) in rack_pos_dict.keys():
                        #later on I will need to break this out into multiple columns
                        #for now this will show rack position number and device name at that position
                        curr_device_str = "{} {}".format(self.maxRackHeight-i,rack_pos_dict[str(self.maxRackHeight - i)])
                        #used to get device name on its own, might be unnecessary later
                        curr_device_key = rack_pos_dict[str(self.maxRackHeight - i)]
                        #create a temporary qlabel object so I can give it a background color
                        label = QLabel(curr_device_str)
                        label.setStyleSheet("QLabel { background-color : silver; color : black; }")
                        #Tool tip accepts RTF style
                        label.setToolTip("Model: {}\r\nPower: {} W".format(main_dict[curr_device_key]['model'], main_dict[curr_device_key]['power']))
                        self.layout.addWidget(label, i, j)
                    else:
                        #This will be all I need to print the numbers
                        label = QLabel(str(self.maxRackHeight - i))
                        label.setStyleSheet("QLabel { background-color : silver; color : black; }")
                        self.layout.addWidget(label, i, j)

                else:
                    self.layout.addWidget(QLabel(""), i, j)

    #open file and display contents
    #file open gives an error that can be ignored on Mac
    def viewRack(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            print("Clearing old rack")
            self.clearGridLayout()
            self.horizontalGroupBox.setTitle("Rack File: {}".format(fname[0]))
            f = open(fname[0], 'r')
            #call class object here
            #main_root = open_file(f)
            #main_dict = save_vals_to_nested_dict(main_root)

            main_root = self.curr_rack.open_file(f)
            main_dict = self.curr_rack.save_vals_to_nested_dict()
            #main_dict = self.curr_rack.save_vals_to_nested_dict(main_root)
            #main_list has the indices where each device will be mounted on the rack
            main_list = build_rack(main_dict)
            self.printRack_GUI(main_list, main_dict)

    def addToRack(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            self.horizontalGroupBox.setTitle("Rack File: {}".format(fname[0]))
            f = open(fname[0], 'r')
            main_root = open_file(f)
            main_dict = save_vals_to_nested_dict(main_root)
            self.clearGridLayout()
            main_list = build_rack(main_dict)
            self.printRack_GUI(main_list, main_dict)

            #changed this function for GUI input
            new_main_dict = self.add_dev_gui(main_dict)

            if new_main_dict:
                #print_rack(new_main_dict)
                new_main_list = build_rack(new_main_dict)
                self.printRack_GUI(new_main_list, new_main_dict)
                reply = QMessageBox.question(self, 'Save File', 'Would you like to save this file?', QMessageBox.No | QMessageBox.Yes, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    print('Saving')
                    self.write_file_from_dict_gui(new_main_dict)
                else:
                    print('Not saving')
                    self.clearGridLayout()
                    self.printRack_GUI(main_list, main_dict)

    def removeFromRack(self):
        print('Remove from rack')

        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            self.horizontalGroupBox.setTitle("Rack File: {}".format(fname[0]))
            f = open(fname[0], 'r')
            main_root = open_file(f)
            main_dict = save_vals_to_nested_dict(main_root)
            self.clearGridLayout()
            main_list = build_rack(main_dict)
            self.printRack_GUI(main_list, main_dict)

            new_main_dict = self.remove_dev_gui(main_dict)

            #check to see if a device wa successfully removed
            if new_main_dict:
                #self.promptSave(new_main_dict)
                #print_rack(new_main_dict)
                new_main_list = build_rack(new_main_dict)
                #print(new_main_list)
                self.clearGridLayout()
                self.printRack_GUI(new_main_list, new_main_dict)
                reply = QMessageBox.question(self, 'Save File', 'Would you like to save this file?', QMessageBox.No | QMessageBox.Yes, QMessageBox.Yes)
                if reply == QMessageBox.Yes:
                    print('Saving')
                    self.write_file_from_dict_gui(new_main_dict)
                else:
                    print('Not saving')
                    main_dict = save_vals_to_nested_dict(main_root)
                    self.clearGridLayout()
                    main_list = build_rack(main_dict)
                    self.printRack_GUI(main_list, main_dict)

    def quitProgram(self):
        qApp.quit()

    #used by add to rack, has user input boxes for needed fields
    #later, add all inputs to one box?
    def add_dev_gui(self, dev_dict):
        #return old_dict if the device could not be added
        #or false if the user does not click ok on input box

        temp_name, ok_name = QInputDialog.getText(self, 'Add Device', 'Device Name: ')
        #if user does not click Ok exit this add menu
        if not ok_name:
            return False

        temp_model, ok_model = QInputDialog.getText(self, 'Add Device', 'Device Model: ')
        if not ok_model:
            return False

        temp_rack_u, ok_rack_u = QInputDialog.getText(self, 'Add Device', 'Device Height: ')
        if not ok_rack_u:
            return False

        temp_start, ok_start = QInputDialog.getText(self, 'Add Device', 'Starting Rack Shelf: ')
        if not ok_start:
            return False

        temp_power, ok_power = QInputDialog.getText(self, 'Add Device', 'Power Consumption(W): ')
        if not ok_model:
            return False

        #count is going to be difficult to use when I start adding devices
        #Need to find current count so I can increment
        curr_max = 0
        for device in dev_dict:
            temp_curr = int(dev_dict[device]['count'])
            if temp_curr > curr_max:
                curr_max = temp_curr

        #increment count by one
        curr_max += 1

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

    def write_file_from_dict_gui(self, dev_dict):
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
        #out_name = input("Enter file name to save as(including .xml)\n>")

        fname = QFileDialog.getSaveFileName(self, 'Save file', '/home', '.xml')
        #print(fname[0])
        if fname[0]:
            #out_name = open(fname[0], 'w+')
            self.horizontalGroupBox.setTitle("Rack File: {}".format(fname[0]))
            #write data to file
            with open(fname[0],'w+') as outfile:
                outfile.write(newxml.toprettyxml(indent='\t',newl='\n'))
                print("\nFile output complete!")

    def remove_dev_gui(self, dev_dict):
        #create a temporary device list
        temp_list = []

        #store current devices on rack in a list to be used for dropdown
        #print("Current Devices:")
        for device in dev_dict:
            #print(device)
            temp_list.append(device)

        #add None so it can be selected from the dropdown
        temp_list.append('None')
        #print(temp_list)
        #temp_dev = input("Which device would you like to remove?\n>")
        temp_dev, ok_dev = QInputDialog.getItem(self, 'Remove Device', 'Select a device to remove: ', temp_list)

        #validate that user wants to remove a device
        if ok_dev:
            if temp_dev in temp_list and temp_dev != 'None':
                del dev_dict[temp_dev]
                print("Device Deleted")
                return dev_dict

        print('No devices removed.')
        return False

    def promptSave(self, new_main_dict):
            print_rack(new_main_dict)
            reply = QMessageBox.question(self, 'Save File', 'Would you like to save this file?', QMessageBox.No | QMessageBox.Yes, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                print('Saving')
                self.write_file_from_dict_gui(new_main_dict)
            else:
                print('Not saving')


class Rack(object):

    def __init__(self):
        print("Creating Rack Object")
        #don't need any inits at this point...

    #open file and store the current root position
    def open_file(self, filename):
        tree = ET.parse(filename)
        #either use this one line or the next two
        #self.curr_root = tree.getroot()

        self.root = tree.getroot()
        #root = tree.getroot()
        #return root

    def save_vals_to_nested_dict(self):
        dev_dict = {}
        #count is not part of the xml file, but may be helpful to know
        count = 0
        for elem in self.root:
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


#########
#OLD Main
#########

#This function opens the provided file and finds the "root" of the XML tree
#may need to rename function
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
    #print('\n\nBuild Rack\n--------------------')
    print('Build Rack')
    #print(dev_dict) Nested dictionary
    #print(f"{dev_dict['RED-2920SW1']['model']}\n") Access single element

    #change later to a larger number
    rack_height = 20
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

    #print(f"Contents of rack(Rack Position:Device Name): {rack_full}")

    return rack_full

def add_dev_console(dev_dict):
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
            new_main_dict = add_dev_console(main_dict)

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
    #main_menu()
    app = QApplication(sys.argv)
    temp = DisplayMain()
    sys.exit(app.exec_())
