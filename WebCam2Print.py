#Only tested on Windows due to VideoCapture module
#Module Requirements:
# *VideoCapture http://videocapture.sourceforge.net/
# *PIL
#
#Uses three files from the same directory as the script:
# *settings.txt - contains replacement fields (e.g. NAME=Please enter name) -
#    each line will occur as a field in the GUI, with the second item as the
#    label. Occurences of the first item (e.g. NAME) are searched in the rtf
#    file (with % either side e.g. %NAME%) and replaced with the value entered
#    into the GUI
# *template.rtf - template rtf file. Use %NAME% or similar (matching the items
#    in the settings) to replace text. After creation the file must be editted
#    in a text editor to change the full path of the placeholder image with just
#    "REPLACEPICTURE.jpg"
# *REPLACEPICTURE.jpg - placeholder picture for template.

__author__ = "Victor Rajewski"
__copyright__ = "Copyright 2012, Victor Rajewski"
__credits__ = ["Victor Rajewski"]
__license__ = "GPL"
__version__ = "0.8"
__email__ = "askvictor@gmail.com"
'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import Tkinter
import Image,ImageOps,ImageTk
import VideoCapture
import win32api,win32print
import tempfile,shutil,os

class WebCam:
    def __init__(self,myParent,
                 updateInterval=50,
                 settingsFile="settings.txt",
                 templateFile="template.rtf",
                 replacePicture="REPLACEPICTURE.jpg"):
        self.updateAfter=updateInterval
        self.parent=myParent
        self.templateFile = templateFile
        self.replacePicture=replacePicture
        f = open(settingsFile)
        self.params = []
        for line in f:
            (parameter,label) = line.strip().split("=")
            self.params.append([parameter,label])

        self.cam=VideoCapture.Device()

        self.label_image=Tkinter.Label(myParent)
        self.label_image.grid(row=0,column=0,columnspan=2)
        currentRow = 1
        for param in self.params:
            label = Tkinter.Label(myParent, text=param[1] + ":")
            label.grid(column=0,row=currentRow,sticky=Tkinter.E)
            entry = Tkinter.Entry(myParent)
            param.append(entry)
            entry.grid(column=1,row=currentRow,sticky=Tkinter.W)
            currentRow += 1
        self.button=Tkinter.Button(myParent,text="Print",command=self.snap)
        self.button.grid(column=0,columnspan=2,row=currentRow)

        self.updateImage()

    def updateImage(self):
        pic=ImageOps.mirror(self.cam.getImage())
        self.tkpi=ImageTk.PhotoImage(pic)
        self.label_image.configure(image=self.tkpi)
        self.parent.after(self.updateAfter,self.updateImage)

    def snap(self):
        imgfile = tempfile.NamedTemporaryFile(suffix=".jpg",delete=False)
        pic = self.cam.getImage()
        pic = ImageOps.mirror(pic)
        pic = pic.resize((320,240))
        pic.save(imgfile,"JPEG")
        template = open(self.templateFile)
        rtffile = tempfile.NamedTemporaryFile(suffix=".rtf",delete=False)
        rtf = template.read()
        for param in self.params:
            rtf = rtf.replace("%" + param[0] + "%", param[2].get())
        #TODO - make this more resilient to changes in the picture path
        rtf = rtf.replace(self.replacePicture,imgfile.name.replace("\\",'\\\\\\\\'))
        rtffile.write(rtf)
        rtffile.close()
        win32api.ShellExecute (0,"print", rtffile.name, None, ".", 0)


root=Tkinter.Tk()

#this can be used to change the tkinter icon
#root.tk.call('wm','iconbitmap',root._w, '-default', 'Webcam.ico')

myapp=WebCam(root)
root.mainloop()
