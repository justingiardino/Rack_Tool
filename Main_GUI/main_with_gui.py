#!/usr/bin/env python3

#add context menu so you can right click a device and edit it
#create a new class for power source? Always going to need wall. Should be similar to Rack class
#Move Rack number to be its own widget
#open file to last location in Explorer/Finder
#when saving new file you have to actually type xml, why?
#drag and drop box
#UPS support

#menu structure
#File > Open New Rack - !
#File > Create New Rack - !
#File > Save Current Rack(Should open to current directory) - !
#File > Quit(Warn before quiting) - !
#Edit > Add device to rack - !
#Edit > Remove Device from Rack - !
#Edit > Edit Device on Rack (Change name, model, power, or location) - !
#View > Rack vs Power?

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
        #used for prompt save for now
        self.rack_open = False
        self.initUI()

    def initUI(self):
        #create a statusBar for display later
        self.statusBar()

        #Main menu labels
        menubar = self.menuBar()
        self.fileMenu =  menubar.addMenu('File')
        self.editMenu = menubar.addMenu('Edit')

        #Create Actions
        self.openAct = QAction('Open Rack', self)
        self.newAct = QAction('Add Device to Rack', self)
        self.remAct = QAction('Remove Device from Rack', self)
        self.quitAct = QAction('Leave Program', self)#Mac doesn't like Quit keyword
        self.saveAct = QAction('Save', self)
        self.modifyAct = QAction('Modify Device on Rack', self)

        #connect actions to functions
        self.openAct.triggered.connect(self.openRack)
        self.newAct.triggered.connect(self.addToRack)
        self.remAct.triggered.connect(self.removeFromRack)
        self.quitAct.triggered.connect(self.quitProgram)
        self.saveAct.triggered.connect(self.saveRack)
        self.modifyAct.triggered.connect(self.modifyDevice)

        #add actions to file menu
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addAction(self.quitAct)

        #create grid for display
        self.createGridLayout()
        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        #make this the central widget of the main menu
        self.setCentralWidget(self.horizontalGroupBox)

        #change these values from the init area
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
                        #create string to be displayed in tool tip
                        tool_str = ""
                        for temp_key in self.new_rack.name_key.keys():
                            #print(temp_key)
                            tool_str += "{}: {}\r\n".format(temp_key, main_dict[curr_device_key][self.new_rack.name_key[temp_key]])

                        label.setToolTip(tool_str)
                        #label.setToolTip("Model: {}\r\nPower: {} W".format(main_dict[curr_device_key]['model'], main_dict[curr_device_key]['power']))
                        self.layout.addWidget(label, i, j)
                    #add an elif here for UPS position
                    #elif tr(self.maxRackHeight - i) in ups_pos_dict.keys():
                    else:
                        #This will be all I need to print the numbers
                        label = QLabel(str(self.maxRackHeight - i))
                        label.setStyleSheet("QLabel { background-color : silver; color : black; }")
                        self.layout.addWidget(label, i, j)

                else:
                    self.layout.addWidget(QLabel(""), i, j)

    #open file and display contents
    #file open gives an error that can be ignored on Mac
    def openRack(self):

        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            print("Clearing old rack")
            self.clearGridLayout()
            self.horizontalGroupBox.setTitle("Rack File: {}".format(fname[0]))
            f = open(fname[0], 'r')
            self.curr_rack.open_file(f)
            self.curr_rack.build_rack()
            self.new_rack = self.curr_rack
            print("Just called build_rack, now calling printRack_GUI")
            self.printRack_GUI(self.curr_rack.rack_full, self.curr_rack.dev_dict)

        #adding these menu options since they weren't valid earlier
        self.editMenu.addAction(self.newAct)
        self.editMenu.addAction(self.remAct)
        self.fileMenu.addAction(self.saveAct)
        self.editMenu.addAction(self.modifyAct)

        self.fileMenu.addAction(self.quitAct)
        self.rack_open = True


    def addToRack(self):
        print("addToRack")
        #self.new_rack = self.curr_rack
        if self.add_dev_gui():
            self.new_rack.build_rack()
            print("new rack list before printing to gui")
            print(self.new_rack.rack_full)
            print(self.curr_rack.rack_full)
            #self.curr_rack = self.new_rack
            self.printRack_GUI(self.new_rack.rack_full, self.new_rack.dev_dict)


    def removeFromRack(self):
        print('removeFromRack')
        #self.new_rack = self.curr_rack
        #self.new_rack.dev_dict = self.remove_dev_gui()
        if self.remove_dev_gui():
            self.new_rack.build_rack()
            #self.curr_rack = self.new_rack
            self.printRack_GUI(self.new_rack.rack_full, self.new_rack.dev_dict)

    def modifyDevice(self):
        print("modifyDevice")
        if self.modify_dev_gui():
            self.new_rack.build_rack()
            #self.curr_rack = self.new_rack
            self.printRack_GUI(self.new_rack.rack_full, self.new_rack.dev_dict)


    def quitProgram(self):
        if self.rack_open:
            self.promptSave()
        qApp.quit()

    def saveRack(self):
        print('Saving')
        self.write_file_from_dict_gui(self.new_rack.dev_dict)

    #used by add to rack, has user input boxes for needed fields
    #later, add all inputs to one box?
    def add_dev_gui(self):
        #or false if the user does not click ok on input box
        print("add_dev_gui")

        for temp_key in self.new_rack.name_key.keys():
            #print(temp_key)
            new_val, ok_val = QInputDialog.getText(self, 'Add Device', temp_key)
            if not ok_val:
                return False

            #If we are adding the name of the device, need to create a new dict
            if temp_key == 'Device Name':
                temp_name = new_val
                self.new_rack.dev_dict[temp_name] = {}
                self.new_rack.dev_dict[temp_name].update({'name':temp_name})
            #all other attributes just need to be added to dict
            else:
                self.new_rack.dev_dict[temp_name].update({self.new_rack.name_key[temp_key]:new_val})

        # temp_name, ok_name = QInputDialog.getText(self, 'Add Device', 'Device Name: ')
        # #if user does not click Ok exit this add menu
        # if not ok_name:
        #     return False
        #
        # temp_model, ok_model = QInputDialog.getText(self, 'Add Device', 'Device Model: ')
        # if not ok_model:
        #     return False
        #
        # temp_rack_u, ok_rack_u = QInputDialog.getText(self, 'Add Device', 'Device Height: ')
        # if not ok_rack_u:
        #     return False
        #
        # temp_start, ok_start = QInputDialog.getText(self, 'Add Device', 'Starting Rack Shelf: ')
        # if not ok_start:
        #     return False
        #
        # temp_power, ok_power = QInputDialog.getText(self, 'Add Device', 'Power Consumption(W): ')
        # if not ok_model:
        #     return False
        #
        # self.new_rack.dev_dict[temp_name] = {}
        # self.new_rack.dev_dict[temp_name].update({'name':temp_name})
        # self.new_rack.dev_dict[temp_name].update({'model':temp_model})
        # self.new_rack.dev_dict[temp_name].update({'rack_u':temp_rack_u})
        # self.new_rack.dev_dict[temp_name].update({'rack_start':temp_start})
        # self.new_rack.dev_dict[temp_name].update({'power':temp_power})


        #print("Checking to see if this will fit in the rack.\n")
        #if(self.new_rack.valid_rack):
            #print(f"\n\nNew information successfully added: {self.new_rack.dev_dict[temp_name]}")
            #this section might not be necessary
        return True

        #else:
            #print("Error, could not add device")
            #return False

    #Remove a device from the rack from dropdown, no need for validation on user input
    def remove_dev_gui(self):
        #create a temporary device list
        temp_list = []

        #store current devices on rack in a list to be used for dropdown
        #print("Current Devices:")
        for device in self.new_rack.dev_dict:
            #print(device)
            temp_list.append(device)

        #add None so it can be selected from the dropdown
        temp_list.append('None')
        temp_dev, ok_dev = QInputDialog.getItem(self, 'Remove Device', 'Select a device to remove: ', temp_list)

        #validate that user wants to remove a device
        if ok_dev:
            if temp_dev in temp_list and temp_dev != 'None':
                del self.new_rack.dev_dict[temp_dev]
                print("Device Deleted")
                return True
                #return self.new_rack.dev_dict

        print('No devices removed.')
        return False

    def modify_dev_gui(self):
        #create a temporary device list
        temp_list = []

        #store current devices on rack in a list to be used for dropdown
        #print("Current Devices:")
        for device in self.new_rack.dev_dict:
            #print(device)
            temp_list.append(device)

        #add None so it can be selected from the dropdown
        temp_list.append('None')
        temp_dev, ok_dev = QInputDialog.getItem(self, 'Modify Device', 'Select a device to modify: ', temp_list)

        #validate that user wants to modify a device
        if ok_dev:
            if temp_dev in temp_list and temp_dev != 'None':
                #print(self.new_rack.dev_dict[temp_dev].keys())
                modify_list = list(self.new_rack.name_key.keys())
                print(modify_list)
                modify_list.append('None')
                #remove_list = ['Device Name', 'Device Model', 'Device Height', 'Starting Rack Shelf', 'Power Consumption(w)', 'None']
                temp_modify_att, ok_modify_att = QInputDialog.getItem(self, 'Modify Device', 'Select which attribute to modify: ', modify_list)
                if ok_modify_att and temp_modify_att != 'None':
                    #updating the name is going to be a disaster, that's the name of the dictionary
                    if temp_modify_att == 'Device Name':
                        temp_modify_name, ok_modify_name = QInputDialog.getText(self, 'Set New Value', 'Device Name')
                        if not ok_modify_name:
                            return False

                        #need to update name of dictionary, set new dictionary equal to old, then delete old
                        self.new_rack.dev_dict[temp_modify_name] = self.new_rack.dev_dict[temp_dev]
                        del self.new_rack.dev_dict[temp_dev]
                        self.new_rack.dev_dict[temp_modify_name]['name'] = temp_modify_name

                    else:
                        temp_modify_val, ok_modify_val = QInputDialog.getText(self, 'Set New Value', temp_modify_att)
                        if not ok_modify_val:
                            return False
                        print(temp_modify_val)
                        self.new_rack.dev_dict[temp_dev].update({self.new_rack.name_key[temp_modify_att]:temp_modify_val})

                print("Device modified")
                return True
                #return self.new_rack.dev_dict

        print('No devices modified.')
        return False

    #translate to name_key
    def write_file_from_dict_gui(self, dev_dict):
        #Element arguments (tag, attrib={})
        out_root = ET.Element('devices')
        #SubElement arguments (parent, tag, attrib={})
        # for device in dev_dict:
        #     out_device = ET.SubElement(out_root, 'device', {'name':device})
        #
        #     out_model = ET.SubElement(out_device,'model')
        #     out_model.text = dev_dict[device]['model']
        #
        #     out_rack_u = ET.SubElement(out_device, 'rack_u')
        #     out_rack_u.text = dev_dict[device]['rack_u']
        #
        #     out_rack_start = ET.SubElement(out_device, 'rack_start')
        #     out_rack_start.text = dev_dict[device]['rack_start']
        #
        #     out_power = ET.SubElement(out_device, 'power')
        #     out_power.text = dev_dict[device]['power']

        for device in dev_dict:
            for temp_key in self.new_rack.name_key.keys():
                #print(temp_key)

                if temp_key == 'Device Name':
                    out_device = ET.SubElement(out_root, 'device', {'name':device})

                #all other attributes just need to be added to dict
                else:
                    out_temp = ET.SubElement(out_device, self.new_rack.name_key[temp_key])
                    out_temp.text = dev_dict[device][self.new_rack.name_key[temp_key]]

        #create xml string using ET
        xmlstr = ET.tostring(out_root).decode()
        #format xml string so it is not a flat file
        newxml = MD.parseString(xmlstr)


        fname = QFileDialog.getSaveFileName(self, 'Save file', '/home', '.xml')
        #print(fname[0])
        if fname[0]:
            self.horizontalGroupBox.setTitle("Rack File: {}".format(fname[0]))
            #write data to file
            with open(fname[0],'w+') as outfile:
                outfile.write(newxml.toprettyxml(indent='\t',newl='\n'))
                print("\nFile output complete!")


    #called by quit program
    def promptSave(self):
            #print_rack(new_main_dict)
            reply = QMessageBox.question(self, 'Save File', 'Would you like to save this file?', QMessageBox.No | QMessageBox.Yes, QMessageBox.Yes)
            if reply == QMessageBox.Yes:
                self.saveRack()
            else:
                print('Not saving')

#rack object
#keeps track of the racks root for xml parsing, dictionary containing all values found in the xml file
class Rack(object):

    def __init__(self):
        self.dev_dict = {}
        #valid rack will be used in build_rack function
        self.valid_rack = True
        #add support for adding more attributes to name_key
        self.name_key = {'Device Name':'name', 'Device Model':'model', 'Device Height':'rack_u', 'Starting Rack Shelf':'rack_start', 'Power Consumption(w)':'power', 'Power Source': 'power_source'}

    #open file and store the current root position
    def open_file(self, filename):
        tree = ET.parse(filename)

        self.root = tree.getroot()

        self.dev_dict = {}
        for elem in self.root:
            #add name to dictionary, first declare the nested dictionary
            self.dev_dict[elem.attrib['name']] = {}
            #then adds first entry to the nested dictionary
            self.dev_dict[elem.attrib['name']].update(elem.attrib)
            #loop through all elements and add them to the nested dictionary
            for subelem in elem:
                #dictionary entry with tag and text
                temp_dict = {subelem.tag:subelem.text}
                #add to end of nested dictionary
                self.dev_dict[elem.attrib['name']].update(temp_dict)

#this function will place all devices on the rack, checking to make sure there is space
#if there is no more space display an erorr and list the devices that collide
#put power calculation in another function
#returns True if there was enough room in the rack, False if there is no room
    def build_rack(self):
        #print('\n\nBuild Rack\n--------------------')
        print('Build Rack - New')
        #change later to a larger number
        rack_height = 20
        #format {rack start position:name}
        print(self.dev_dict)
        self.rack_full = {}
        for device in self.dev_dict:
            #check if rack is full at position where device is going
            #will need to add size check later

            #check to see if height is one, or greater than one
            if self.dev_dict[device]['rack_u'] == '1':
                if self.dev_dict[device]['rack_start'] not in self.rack_full.keys():
                    self.rack_full[self.dev_dict[device]['rack_start']] = device
                #else already full at that spot, need to error out
                else:
                    print(f"Error, that spot at number {self.dev_dict[device]['rack_start']} is already taken by {self.rack_full[self.dev_dict[device]['rack_start']]}\nCannot place device {device} there!\n")
                    #When this value is false shouldn't print rack and shouldn't allow save
                    self.valid_rack = False
                    return False
            #height not equal 1, may need to alter this later
            else:
                temp_u = self.dev_dict[device]['rack_u']
                temp_pos = self.dev_dict[device]['rack_start']
                temp_count = '1'
                #this loops through and adds a device to the rack multiple times when the height is larger than 1
                while True:
                    #check if current position has already been filled
                    if temp_pos not in self.rack_full.keys():
                        #add device to rack if not full
                        self.rack_full[temp_pos] = device
                        #move current position down one
                        temp_pos = str(int(temp_pos)-1)
                    else:
                        print(f"Error, that spot at number {temp_pos} is already taken by {self.rack_full[temp_pos]}\nCannot place device {device} there!\n")
                        self.valid_rack = False
                        return False

                    #check to see if the device has more U's that need to be added
                    if temp_count != temp_u:
                        temp_count = str(int(temp_count)+1)
                        #print("More space needed")
                    #if all U's of the device have been added leave this while loop
                    elif temp_pos == '0':
                        print("Too low, cannot place device there")
                        self.valid_rack = False
                        return False
                    elif temp_count == temp_u:
                        print("Done adding device")
                        #print(self.rack_full)
                        self.valid_rack = True
                        #return True
                        break
                    else:
                        print("Rack full")#Why does this print rack full on first iteration?
                        self.valid_rack = False
                        return False

            #won't need this print in the end, this is for debugging
            #print(f"Count: {dev_dict[device]['count']}\nDevice: {device}\nModel: {dev_dict[device]['model']}\nPower: {dev_dict[device]['power']} Amps\nRack U: {dev_dict[device]['rack_u']}\nRack Start: {dev_dict[device]['rack_start']}\n")

        print(f"Contents of rack(Rack Position:Device Name):\n {self.rack_full}")

        #return rack_full
        self.valid_rack = True

#create this as a flyout under edit, one per device
class Power(object):
    def __init__(self):
        self.power_dict = {}
        #what do I need to know about power devices
        #devices connected - this will be from a function
        #current usage - calculate this
        #total capacity - need from user input
        #rack position- need from user input
        #number of outlets - need from user input

if __name__ == '__main__':
    #main_menu()
    app = QApplication(sys.argv)
    temp = DisplayMain()
    sys.exit(app.exec_())
