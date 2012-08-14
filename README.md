WebCam2Print was created for a student interview process, as a photobooth/kiosk type application. The default webcam is opened and displays the current image on screen. Additionally, some text fields are shown (these can be defined in the settings file). When the print button is pressed, an RTF template file is used to create a new file, with field replacements for the entered data, and a picture replacement for the current webcam image. This is then sent to the default printer.

Requirements:
* Windows
* Python 2.x (tested on 2.7)
* VideoCapture module from http://videocapture.sourceforge.net/
* PIL module
